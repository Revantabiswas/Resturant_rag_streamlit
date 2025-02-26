import os
import pdfplumber
import re
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st

def load_environment():
    load_dotenv()

def get_max_capacity():
    pdf_path = "Resturant_rag_streamlit/restaurant_docs/restaurant_policy.pdf"
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                match = re.search(r"Max Capacity:\s*(\d+)", text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
    except Exception as e:
        print(f"Error reading max capacity from PDF: {e}")
    # Return a default capacity if not found
    return 50

def initialize_knowledge_base():
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        pdf_directory = "Resturant_rag_streamlit/restaurant_docs"
        all_text = []
        for pdf_file in os.listdir(pdf_directory):
            if pdf_file.endswith(".pdf"):
                with pdfplumber.open(os.path.join(pdf_directory, pdf_file)) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            all_text.append(text)
        if not all_text:
            st.sidebar.error("No text extracted from PDFs. Please check the documents and retry.")
        else:
            combined_text = "\n".join(all_text)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            final_documents = text_splitter.split_text(combined_text)
            vectors = FAISS.from_texts(final_documents, embeddings)
            st.session_state.vectors = vectors
            st.session_state.vector_ready = True
            st.sidebar.success("Knowledge Base Initialized!")
    except Exception as e:
        st.sidebar.error(f"Error initializing: {e}")
