import openai
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.llms import OpenAI  # Use the correct module for OpenAI
from decouple import config  # Import config from python-decouple

# Load API keys from the .env file
openai_api_key = config('OPENAI_API_KEY')
pinecone_api_key = config('PINECONE_API_KEY')
pinecone_index_name = config('PINECONE_INDEX')

# Set up OpenAI (this only needs to be done once)
llm = OpenAI(temperature=0.0)

# Set up Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Check if the index exists, and create if it doesn't
if pinecone_index_name not in pc.list_indexes().names():
    pc.create_index(
        name=pinecone_index_name,
        dimension=1536,  # Adjust the dimension based on your use case
        metric='euclidean',  # Or other metric as needed
        spec=ServerlessSpec(cloud='aws', region='us-east-1')  # Use your correct cloud/region
    )

index = pc.Index(pinecone_index_name)

# Example LangChain interaction for RAG
def your_rag_function(query):
    # Process the query using LangChain (OpenAI LLM) and Pinecone
    result = llm(query)
    
    # If Pinecone interaction is needed, you can store/retrieve vectors
    # For example: index.upsert([("id", vector)])
    
    return result
