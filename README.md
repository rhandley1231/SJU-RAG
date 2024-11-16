# SJU-RAG
This repository is for the CUS 690 Capstone class, building a RAG application for the St John's Website.  This project utilizes LangChain, OpenAI's LLM API's, and Pinecone for advanced vector search.  Combined with Django for a scalable, resilent backend and an intuitive React UI, we provice seamless AI-driven knowledge access.
  
## Stack ##
- React frontend
- Django backend
- Pinecone database

## Team ##
- Ryan: Team Leader, Full Stack 
- Jomo: Full Stack
- Tahir: Full Stack
- Shanbin: Full Stack
- Elena: Backend & Databases
- Joshua: Backend & Databases, Project Management
- Jordan: Backend & Databases, Project Management

### Steps to Reproduce ###
- APIs:
    - You'll need to create a `.env` file containing your own API keys.  You'll need the following:
        - OpenAI API Key
        - Pinecone API Key
        - Pinecone Index Name
- Frontend Reproduction:
    - Run `npm install` in the RAG-Frintend directory
    - Run `npm run dev` to start the frontend
- Backend Reproduction:
    - Ensure you are using Python version 3.9.18
    - In the main directory -- `SJU-Rag` -- run `source venv/bin/activate` to activate the virtual environment
    - Cd into the backend folder and run `python manage.py runserver` to start the backend