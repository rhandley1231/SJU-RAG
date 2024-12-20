from langchain_openai import ChatOpenAI
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
google_api_key = os.environ.get('GOOGLE_API_KEY')
google_cse_id = os.environ.get('GOOGLE_CSE_ID')

# Initialize the Google Search wrapper with custom CSE
google_search = GoogleSearchAPIWrapper()

# Initialize the ChatOpenAI model
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name='gpt-3.5-turbo',
    temperature=0.2
)

# Global session storage for chat histories
session_store = {}

# Define the global system prompt
SYSTEM_PROMPT = SystemMessage(
    content='''
    You are a helpful and friendly assistant specializing in university-related topics. 
    Provide concise, accurate answers based on retrieved information, and prioritize clarity. 
    If the user's question is unclear, off-topic, or outside your expertise, respond in a conversational, polite, and encouraging manner. 
    Gently guide the user back to relevant university-related topics if possible.
    '''
)

def get_session_history(session_id):
    """Retrieve or initialize chat history for a session."""
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
        session_store[session_id].add_message(SYSTEM_PROMPT)
    return session_store[session_id]

def google_search_query(question, num_results=4):
    """
    Use Google Custom Search API to find information.
    Returns a list of results with 'title', 'snippet', 'link' if available.
    Otherwise returns a string indicating no results.
    """
    search_results = google_search.results(question, num_results=num_results)
    if not search_results or not isinstance(search_results, list):
        return "No relevant results were found on Google."
    
    processed_results = []
    for res in search_results:
        title = res.get("title", None)
        snippet = res.get("snippet", None)
        link = res.get("link", None)
        
        # If any of these fields are missing, skip this result
        if title and snippet and link:
            processed_results.append({
                "title": title,
                "snippet": snippet,
                "link": link
            })
    
    if not processed_results:
        return "No relevant results were found on Google."
    
    return processed_results

def conversational_rag(question, session_id=None):
    """
    Handles a conversational query using Google Search for retrieval and always considers chat history for responses.
    """
    # Generate a new session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    # Retrieve or initialize chat history for this session
    chat_history = get_session_history(session_id)

    # Add the user's question to the chat history
    chat_history.add_user_message(question)

    # Retrieve recent chat history for context
    recent_context = "\n".join(
        f"User: {msg.content}" if isinstance(msg, HumanMessage)
        else f"Assistant: {msg.content}"
        for msg in chat_history.messages[-6:]
    )

    # Perform Google Search to retrieve relevant information
    google_results = google_search_query(question, num_results=4)

    # Check if google_results is a string (indicating no results) or if results are just not relevant
    if isinstance(google_results, str):
        # Use the LLM to generate a helpful and encouraging response
        llm_input = (
            f"You are Johnny Bot, a friendly and intelligent assistant. The following is a recent conversation:\n\n"
            f"{recent_context}\n\n"
            f"The user just asked: '{question}'\n\n"
            "No relevant results were found on Google. According to the system instructions, respond in a helpful, "
            "friendly way and encourage the user to refine their query or provide more context. Gently redirect them "
            "toward university-related topics if possible."
        )
        response_content = llm.predict(llm_input)
        
        # Add the assistant's response to the chat history
        chat_history.add_ai_message(f'<div class="bot-message">{response_content}</div>')
        
        # Format chat history for the frontend
        formatted_history = [
            {"role": "user", "content": msg.content} if isinstance(msg, HumanMessage)
            else {"role": "assistant", "content": msg.content}
            for msg in chat_history.messages
        ]
        
        return {
            'answer': response_content,
            'chat_history': formatted_history,
            'session_id': session_id
        }

    # If results are found, process and format them
    search_results = [
        f"{result['title']}: {result['snippet']} (Source: {result['link']})"
        for result in google_results
    ]
    search_results_text = "\n\n".join(search_results)

    # Use chat history and search results to generate a response
    llm_input = (
        f"You are Johnny Bot, a friendly and intelligent assistant. The following is a recent conversation:\n\n"
        f"{recent_context}\n\n"
        f"Additional information retrieved from the web:\n\n"
        f"{search_results_text}\n\n"
        f"Given the context of the conversation and the retrieved information, answer the user's latest question accurately, concisely, and in great detail:\n\n"
        f"Question: {question}\n\n"
        f"Provide a highly descriptive, clear, factual, and friendly response. Don't worry about including links."
    )
    response_content = llm.predict(llm_input)

    # Include sources in the response
    sources_list = "\n".join(
        f'<a href="{result["link"]}" target="_blank">{result["title"]}</a>'
        for result in google_results
    )
    response_content += f"\n\nSources:\n\n{sources_list}"

    # Add the assistant's response to the chat history
    chat_history.add_ai_message(f'<div class="bot-message">{response_content}</div>')

    # Format chat history for the frontend
    formatted_history = [
        {"role": "user", "content": msg.content} if isinstance(msg, HumanMessage)
        else {"role": "assistant", "content": msg.content}
        for msg in chat_history.messages
    ]

    return {
        'answer': response_content,
        'chat_history': formatted_history,
        'session_id': session_id
    }