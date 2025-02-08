import streamlit as st
import os
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import PyPDF2  

def vectorstore(uploaded_file, vAR_api_key):   
    # Create 'files' directory if it doesn't exist
    FILES_DIR = "files"
    os.makedirs(FILES_DIR, exist_ok=True)

    file_path = os.path.join(FILES_DIR, uploaded_file.name)  # Save inside 'files/' directory
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read()) 

    def extract_text_from_pdf(pdf_path):
        """Extracts text from a PDF using PyPDF2."""
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""  # Extract text from each page
        return text

    extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text.strip():
        st.error("❌ No text could be extracted from the PDF. Try another file.")
    else:
        # Split text into chunks for embedding
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.create_documents([extracted_text])

        # Generate embeddings using OpenAI
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(texts, embeddings)

        # Create Chat Model
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        retriever = vector_store.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        return qa_chain

    # Chat Interface
def get_response(query, qa_chain):
    response = qa_chain.run(query)
    return response