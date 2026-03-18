import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")


PROMPT_TEMPLATE = """
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Instructions:
- Write the answer in 3-5 bullet points
- Use simple words a 5th grade child can understand
- Do not add information outside the context
"""

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
)

# Vector database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chroma_path = os.path.join(BASE_DIR, "chroma_db")

db = Chroma(
    persist_directory=chroma_path,
    embedding_function=embeddings
)

retriever = db.as_retriever(search_kwargs={"k":5})

# Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY
)

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# Format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def rag_engine(query_text):

    docs = retriever.invoke(query_text)

    context = format_docs(docs)

    response = rag_chain.invoke(query_text)

    sources = set()
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        file_name = os.path.basename(source)
        # remove .pdf
        title = file_name.replace(".pdf", "")

        # replace underscores if any
        title = title.replace("_", " ")

       # make title look nice
        title = title.title()

        sources.add(f"{title} — Page {page}")

    sources = sorted(list(sources))

    return response, sources
    #print(response)
    #print(sources)

#rag_engine("How to let elders have a healthy diet")


