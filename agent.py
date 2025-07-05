# importing necessary libraries 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
load_dotenv()
serp_api_key=os.getenv("Serp_api_key")

pdf_path=input("enter the pdf path")
def process_pdf(pdf_path):
    loader=PyPDFLoader(pdf_path)
    docs=loader.load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=50)
    chunks=splitter.split_documents(docs)
    return chunks
documents=process_pdf(pdf_path)
