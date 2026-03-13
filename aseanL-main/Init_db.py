from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import shutil
import os

DATA_PATH = "data"

def generate_data_store():
    pages = load_pdf()
    chunks = split_pdf(pages)
    save_to_chroma(chunks)

def load_pdf():
    pages = []

    if not os.path.exists(DATA_PATH):
        print(f"Error: Data directory '{DATA_PATH}' not found.")
        return []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_PATH, file))
            pages.extend(loader.load())

    return pages

def split_pdf(pages):
    if not pages:
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(pages)
    return chunks

pages = load_pdf()
chunks = split_pdf(pages)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def save_to_chroma(chunks):
    if not chunks:
        print("No chunks to save.")
        return

    chroma_path = 'chroma_db'
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)

    db = Chroma.from_documents(chunks, embeddings, persist_directory=chroma_path)
    # db.persist() is no longer required in newer Chroma versions
    print(f"Saved {len(chunks)} chunks to {chroma_path}")

generate_data_store()