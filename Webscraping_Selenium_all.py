import pdfplumber 
from docx import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import os

with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

output_file = "stjohns_content.txt"

def download_file(url, path):
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification or we will run into an exception
        response.raise_for_status() 
        with open(path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully: {path}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading {url}: {e}")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
    return text if text.strip() else None  

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text if text.strip() else None  
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied for the file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while extracting text from '{file_path}': {e}")
    return None  

with open(output_file, "w") as file:
    for url in urls:
        driver.get(url)
        time.sleep(2)  

        soup = BeautifulSoup(driver.page_source, "html.parser")

        text_content = soup.get_text(separator="\n", strip=True)

        file.write(f"URL: {url}\n\n")
        file.write(text_content)
        file.write("\n\n" + "=" * 80 + "\n\n")

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.endswith(".pdf") or href.endswith(".docx"):
                file_url = href if href.startswith("http") else url + href
                file_name = os.path.join(download_dir, file_url.split("/")[-1])

                download_file(file_url, file_name)

                if file_name.endswith(".pdf"):
                    text_content = extract_text_from_pdf(file_name)
                elif file_name.endswith(".docx"):
                    text_content = extract_text_from_docx(file_name)

                if text_content:
                    file.write(f"File: {file_name}\n\n")
                    file.write(text_content)
                    file.write("\n\n" + "=" * 80 + "\n\n")
                else:
                    print(f"No text was extracted from {file_name}.")

driver.quit()
