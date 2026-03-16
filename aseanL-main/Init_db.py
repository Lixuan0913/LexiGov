import fitz
import pytesseract
from PIL import Image
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import shutil
import os
import re
import json

DATA_PATH = "./data"


def generate_data_store():
    pages = load_pdf()
    sections = split_by_section(pages)
    chunks = split_chunks(sections)

    save_to_json(chunks)   
    save_to_chroma(chunks)


# -----------------------------
# TEXT CLEANING
# -----------------------------
def clean_text(text):

    if not text:
        return ""

    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"Page\s*\d+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    lines = text.split("\n")
    lines = [line.strip() for line in lines if len(line.strip()) > 3]

    return "\n".join(lines).strip()


# -----------------------------
# LOAD PDF
# -----------------------------
def load_pdf():

    pages = []

    if not os.path.exists(DATA_PATH):
        print(f"Error: Data directory '{DATA_PATH}' not found.")
        return []

    for root, dirs, files in os.walk(DATA_PATH):

        for file in files:

            if file.endswith(".pdf"):

                file_path = os.path.join(root, file)
                print("Loading:", file_path)

                pdf = fitz.open(file_path)

                for page_num, page in enumerate(pdf):

                    text = page.get_text()

                    # OCR if empty
                    if not text.strip():

                        pix = page.get_pixmap()

                        img = Image.frombytes(
                            "RGB",
                            [pix.width, pix.height],
                            pix.samples
                        )

                        text = pytesseract.image_to_string(img)

                    text = clean_text(text)

                    if len(text) < 50:
                        continue

                    pages.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": file_path,
                                "page": page_num
                            }
                        )
                    )

    print("Total pages loaded:", len(pages))
    return pages


# -----------------------------
# SPLIT BY SECTION
# -----------------------------
def split_by_section(pages):

    section_docs = []

    for page in pages:

        text = page.page_content

        sections = re.split(r"\n\s*Section\s+\d+", text)

        for sec in sections:

            if len(sec.strip()) > 50:

                section_docs.append(
                    Document(
                        page_content=sec.strip(),
                        metadata=page.metadata
                    )
                )

    print("Total sections created:", len(section_docs))
    return section_docs


# -----------------------------
# SPLIT CHUNKS
# -----------------------------
def split_chunks(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(docs)

    print("Total chunks created:", len(chunks))

    return chunks


# -----------------------------
# EMBEDDINGS
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# -----------------------------
# SAVE JSON DATASET
# -----------------------------
def save_to_json(chunks):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(BASE_DIR, "dataset.json")

    data = []

    for i, chunk in enumerate(chunks):

        data.append({
            "id": i,
            "text": chunk.page_content,
            "source": chunk.metadata.get("source", ""),
            "page": chunk.metadata.get("page", "")
        })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved JSON dataset:", json_path)


# -----------------------------
# SAVE CHROMA VECTOR DB
# -----------------------------
def save_to_chroma(chunks):

    if not chunks:
        print("No chunks to save.")
        return

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    chroma_path = os.path.join(BASE_DIR, "chroma_db")

    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=chroma_path
    )

    db.persist()

    print(f"Saved {len(chunks)} chunks to {chroma_path}")


generate_data_store()