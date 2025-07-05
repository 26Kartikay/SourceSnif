# importing necessary libraries 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from serpapi import GoogleSearch
import os
from difflib import SequenceMatcher

load_dotenv()
serp_api_key=os.getenv("Serp_api_key")

pdf_path="test1.pdf"
#=input("enter the pdf path :")
def process_pdf(pdf_path):
    loader=PyPDFLoader(pdf_path)
    docs=loader.load()
    splitter=RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=50)
    chunks=splitter.split_documents(docs)
    return chunks
documents=process_pdf(pdf_path)
#print(documents)
def search_serpapi(query, api_key):
    params = {
        "q": query[:300],       
        "api_key": api_key,
        "num": 5                
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

def similarity_score(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

SIMILARITY_THRESHOLD = 0.5 

for i, doc in enumerate(documents):
    chunk_text = doc.page_content.strip()
    print(f"\nChecking Document Chunk {i+1} (first 100 chars):\n{chunk_text[:len(documents)]}...")

    try:
        results = search_serpapi(chunk_text, serp_api_key)
    except Exception as e:
        print(f" API Error: {e}")
        continue

    if not results:
        print(" No results returned.")
        continue

    for result in results:
        snippet = result.get("snippet", "")
        score = similarity_score(chunk_text, snippet)

        if score > SIMILARITY_THRESHOLD:
            print("\nPOSSIBLE PLAGIARISM DETECTED:")
            print(f" - Similarity Score: {score:.2f}")
            print(f" - Snippet: {snippet}")
            print(f" - Source Title: {result.get('title', 'N/A')}")
            print(f" - URL: {result.get('link', 'N/A')}")


