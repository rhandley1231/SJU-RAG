# SJU-RAG
This repository is for the CUS 690 Capstone class, building a RAG application for the St John's Website.  This project utilizes LangChain, OpenAI's LLM API's, and Google's Programmable Search Engine to retrieve data and generate concise, relevant, and timely responses.  Combined with Django for a scalable, resilent backend and an intuitive React UI, we provice seamless AI-driven knowledge access.
  
## Stack 
- React frontend
- Django backend

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
    - `OPENAI_API_KEY` (Open AI)[https://platform.openai.com/docs/overview]
    - `GOOGLE_API_KEY` (Google Cloud Platform)[https://console.cloud.google.com/]
    - `GOOGLE_CSE_ID`  (Programmable Search Engine)[https://programmablesearchengine.google.com/]
- Ensure you have suficient funds in your accounts to create the embeddings and to use the model (about $10 in OpenAI if you already use the platforms a lot)

 ### Web Scraping & Index Population
- Create a Programmable Search Engine on Google Cloud Platform and copy the CSE ID it gives you.  Do not use the entire web; just add the following three domains:
```sh
*.studentaid.gov/*
*.torchonline.com/*
*.stjohns.edu/*
```
- Then, create an API key to use with this service through Google Cloud Platform.  Add the key and search engine ID to your .env file.
- You can now use the RAG Model.

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
