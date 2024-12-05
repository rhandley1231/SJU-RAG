from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_google_community import GoogleSearchAPIWrapper
from dotenv import load_dotenv
import uuid
import os

# Load environment variables from .env
load_dotenv()

# API keys
openai_api_key = os.environ.get('OPENAI_API_KEY')
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
pinecone_index_name = os.environ.get('PINECONE_INDEX')
google_api_key = os.environ.get('GOOGLE_API_KEY')
google_cse_id = os.environ.get('GOOGLE_CSE_ID')

# Initialize the Google Search wrapper
google_search = GoogleSearchAPIWrapper()

# Check for required keys
if not openai_api_key or not pinecone_api_key or not pinecone_index_name or not google_api_key or not google_cse_id:
    raise ValueError("API keys and index name must be set as environment variables.")

# Initialize OpenAI and Pinecone
embeddings = OpenAIEmbeddings(api_key=openai_api_key)
vectorstore = PineconeVectorStore(
    index_name=pinecone_index_name,
    embedding=embeddings,
    pinecone_api_key=pinecone_api_key
)

# Initialize the ChatOpenAI model
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name='gpt-3.5-turbo',
    temperature=0.1
)

# Initialize the evaluation LLM
evaluation_llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-3.5-turbo",
    temperature=0
)

# Initialize the retriever from the vector store
retriever = vectorstore.as_retriever()

# Setup the conversational retrieval chain
chatbot_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Global session storage for chat histories
session_store = {}

# Define the global system prompt
SYSTEM_PROMPT = SystemMessage(
    content='''
    You are a helpful assistant specializing in university-related topics.
    Provide concise, accurate answers based on the retrieved information,
    and prioritize clarity while being polite and informative. Provide the 
    link based on the source from the metadata. Retrieve the most 
    recent information available.
    '''
)

def get_session_history(session_id):
    """Retrieve or initialize chat history for a session."""
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
        session_store[session_id].add_message(SYSTEM_PROMPT)
    return session_store[session_id]

def is_response_insufficient_with_llm(question, response):
    """
    Uses an LLM to evaluate if the RAG response is insufficient.
    """
    prompt = f"""
    You are a helpful assistant. I will provide you with a question and a response. 
    Your job is to determine if the response sufficiently answers the question. 

    Question: "{question}"

    Response: "{response}"

    Please answer in the following format:
    Decision: [Yes or No]
    Reason: [Explain why the response is sufficient or insufficient]

    Example:
    Decision: No
    Reason: The response does not provide any specific details about the performers at Stormin' Loud in 2024.
    """
    evaluation = evaluation_llm.invoke([HumanMessage(content=prompt)])
    print("LLM Response:", evaluation.content)  # Debugging: Log the LLM response
    try:
        lines = evaluation.content.split("\n")
        decision = lines[0].replace("Decision:", "").strip()
        reason = lines[1].replace("Reason:", "").strip()
        return decision.lower() == "no", reason
    except (IndexError, ValueError):
        print(f"Unexpected LLM response format: {evaluation.content}")
        return False, "Could not determine sufficiency from LLM response."

def google_fallback_search(question, num_results=2):
    """
    Use Google Search API to find additional information, limiting results to num_results.
    """
    search_results = google_search.results(question, num_results=num_results)
    if not search_results:
        return "No relevant results were found on Google."

    formatted_results = [
        {
            "title": result["title"],
            "snippet": result["snippet"],
            "link": result["link"]
        }
        for result in search_results[:num_results]
    ]
    return formatted_results


def conversational_rag(question, session_id=None):
    """
    Handles a conversational query, using LLM to evaluate RAG responses and fallback to Google Search if necessary.
    """
    # Generate a new session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    # Retrieve or initialize chat history for this session
    chat_history = get_session_history(session_id)

    # Add the user's question to the chat history
    chat_history.add_user_message(question)

    # Query Pinecone using the chatbot chain
    response = chatbot_chain.invoke({
        "question": question,
        "chat_history": chat_history.messages,
    })

    pinecone_answer = response['answer']
    source_documents = response.get('source_documents', [])

    try:
        # Use the LLM to evaluate the response
        is_insufficient, reason = is_response_insufficient_with_llm(question, pinecone_answer)
    except Exception as e:
        print(f"Error during LLM evaluation: {e}")
        is_insufficient = False
        reason = "Defaulting to Pinecone response due to evaluation error."

    if is_insufficient:
        # Perform Google Search as a fallback
        google_results = google_fallback_search(question, num_results=2)
        if isinstance(google_results, str):  # Handle case with no results
            enhanced_response = (
                f"While the St. John's websites don't have this information readily available, "
                f"I couldn't find relevant results on Google either."
            )
        else:
            # Use the top one or two results to build a human-readable response
            sources_text = "<br><br>".join(
                f'<a href="{result["link"]}" target="_blank">{result["title"]}</a>: {result["snippet"]}'
                for result in google_results
            )
            enhanced_response = (
                f"While the St. John's websites don't have this information readily available, "
                f"I found the following from Google:<br><br>{sources_text}"
            )
    else:
        # Use Pinecone's response and format sources
        sources = set(doc.metadata.get('source') for doc in source_documents if doc.metadata.get('source'))
        source_links = "<br>".join(f'<a href="{link}" target="_blank">{link}</a>' for link in sources)
        enhanced_response = pinecone_answer
        if sources:
            enhanced_response += f"<br><br><strong>Sources:</strong><br>{source_links}"

    # Add the assistant's response to the chat history
    chat_history.add_ai_message(f'<div class="bot-message">{enhanced_response}</div>')

    # Format chat history for the frontend
    formatted_history = [
        {"role": "user", "content": msg.content} if isinstance(msg, HumanMessage)
        else {"role": "assistant", "content": msg.content}
        for msg in chat_history.messages
    ]

    return {
        'answer': enhanced_response,
        'chat_history': formatted_history,
        'source_documents': source_documents,
        'session_id': session_id
    }
