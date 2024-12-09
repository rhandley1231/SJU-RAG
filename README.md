# SJU-RAG
This repository is for the CUS 690 Capstone class, building a RAG application for the St John's Website.  This project utilizes LangChain, OpenAI's LLM API's, and Pinecone for advanced vector search.  Combined with Django for a scalable, resilent backend and an intuitive React UI, we provice seamless AI-driven knowledge access.
  
## Stack 
- React frontend
- Django backend
- Pinecone database

## Team 
- Ryan: Team Leader, Full Stack 
- Jomo: Full Stack
- Tahir: Full Stack
- Shanbin: Full Stack
- Elena: Backend & Databases
- Joshua: Backend & Databases, Project Management
- Jordan: Backend & Databases, Project Management

## Steps to Reproduce 
### APIs:
- You'll need to create a `.env` file containing your own API keys.  You'll need the following fields:
    - `OPENAI_API_KEY`
    - `PINECONE_API_KEY`
    - `PINECONE_INDEX`
- Ensure you have suficient funds in your accounts to create the embeddings and to use the model (about $10 in both Pinecone and OpenAI if you already use the platforms a lot)

 ### Web Scraping & Index Population
- Create a Pinecone index on their website using the OpenAI text-embedding-ada-002 embeddings with the cosine metric.  Add the index name as the value for `PINECONE_INDEX` to the .env file mentioned in the APIs section.
- Using the environment.yml file provided, create an Anaconda Environment to run the Notebook with the URL & Web Scraper and Pinecone Loader.
```sh
conda env create -f environment.yml
```
- Verify that the contents are in your index on the pinecone website.
    - If so, you should now be able to run the RAG model using the steps below

### Backend Reproduction:
- Ensure you have Python version 3.9.18 installed
- Create a virtual environment in the main directory -- `SJU-RAG` -- to install your requirements in by running the following
```sh
python3 -m venv venv
```
- Run the following command to activate the virtual environment
```sh
source venv/bin/activate
``` 
- Run the following command to get all the necessary packages installed
```sh
pip install -r requirements.txt
```
- cd into the backend folder and run the following command to start the backend
```sh
python manage.py runserver
```

### Frontend Reproduction:
- Ensure you have Node.js installed on your machine and accessible to your path so you can use node and npm (node pacakge manager).  This is necessary when using JavaScript for Server-Side Development, Local Development, and for CLI tools (you may need to restart your computer after installing and configuring it to be accessible in your path).
- Run the following command in the RAG-Frontend directory to install React specific dependencies
```sh
npm install
```
- Run the following command to start the frontend
```sh
npm run dev
```