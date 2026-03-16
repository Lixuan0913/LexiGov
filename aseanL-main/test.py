from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

data = db.get()

sources = set()

for meta in data["metadatas"]:
    sources.add(meta["source"])

for s in sources:
    print(s)