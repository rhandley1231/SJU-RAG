from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import uuid
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.llms import OpenAI  # Use the correct module for OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Now you can access your variables using os.environ
openai_api_key = os.environ.get('OPENAI_API_KEY')
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
pinecone_index_name = os.environ.get('PINECONE_INDEX')


# Check for required keys
if not openai_api_key or not pinecone_api_key or not pinecone_index_name:
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
    temperature=0.4
)

# Initialize the retriever from the vector store
retriever = vectorstore.as_retriever()

# Setup the conversational retrieval chain
chatbot_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Session storage to manage chat history per session
session_store = {}

def get_session_history(session_id):
    """Retrieve or initialize chat history for a session."""
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()  # Use InMemoryChatMessageHistory for easier handling
    return session_store[session_id]

def conversational_rag(question, session_id=None):
    """Handles a conversational query, storing and using session history."""
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate a new session ID if not provided
    
    # Retrieve or initialize chat history for this session
    chat_history = get_session_history(session_id)

    # Add the user's question to the chat history
    chat_history.add_user_message(question)
    
    # Run the question with the chatbot chain
    response = chatbot_chain.invoke({
        "question": question,
        "chat_history": chat_history.messages  # Use the chat history messages directly
    })
    
    answer = response['answer']
    source_documents = response.get('source_documents', [])
    
    # Add the assistant's response to the chat history
    chat_history.add_ai_message(answer)
    
    # Format chat history as a list of role-content pairs
    formatted_history = [
        ("user", msg.content) if isinstance(msg, HumanMessage) else ("assistant", msg.content)
        for msg in chat_history.messages
    ]
    
    return {
        'answer': answer,
        'chat_history': formatted_history,
        'source_documents': source_documents,
        'session_id': session_id
    }
