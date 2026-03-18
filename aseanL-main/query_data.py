import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import json
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")


PROMPT_TEMPLATE = """
You are LexiGov, a helpful and knowledgeable AI assistant specializing in ASEAN government policies, laws, and public services.
Your goal is to provide clear, accurate, and easy-to-understand answers based strictly on the provided context.

Context Information:
---------------------
{context}
---------------------

User Question: {question}

Instructions for your response:
1. Analyze the context and answer the user's question accurately.
2. Use clear, simple, and accessible language (avoid overly complex legal jargon).
3. Structure your answer well. Use bullet points if it helps break down complex steps or multiple items, but maintain a polite, conversational tone.
4. If the context does not contain the answer to the question, politely state: "I'm sorry, but I couldn't find the specific information regarding your question in the official documents provided." Do NOT make up an answer.
5. CRITICAL: You MUST reply in the exact same language that the user used in their question.

Answer:
"""


# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-small"
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

    # retrieve with similarity score
    results = db.similarity_search_with_score(query_text, k=50)

    # -----------------------------
    # Confidence check
    # -----------------------------
    best_score = results[0][1] if results else 1.0
    CONFIDENCE_THRESHOLD = 0.5

    # -----------------------------
    # Filter relevant docs
    # -----------------------------
    filtered_docs = []
    for doc, score in results:
        if score < 0.55:
            filtered_docs.append(doc)

    # -----------------------------
    # If no relevant docs → NO SOURCES
    # -----------------------------
    no_relevant_docs = len(filtered_docs) == 0

    # fallback (for answer only)
    if no_relevant_docs:
        filtered_docs = [doc for doc, score in results[:3]]

    # -----------------------------
    # Generate response
    # -----------------------------
    context = format_docs(filtered_docs)

    chain = prompt | llm | StrOutputParser()

    import json

    raw_response = chain.invoke({
        "context": context,
        "question": query_text
    })

    try:
        parsed = json.loads(raw_response)
        answer = parsed.get("answer", "")
        found = parsed.get("found", False)
    except:
        answer = raw_response
        found = False

    # -----------------------------
    # Decide sources (🔥 FIX HERE)
    # -----------------------------
    if not found or best_score > CONFIDENCE_THRESHOLD or no_relevant_docs:
        return answer, []   # ✅ ALWAYS EMPTY LIST

    # -----------------------------
    # Build sources
    # -----------------------------
    sources = []
    seen_titles = set()

    for doc in filtered_docs:
        source = doc.metadata.get("source", "Unknown")
        file_name = os.path.basename(source)
        title = file_name.replace(".pdf", "").replace("_", " ").title()

        if title not in seen_titles:
            seen_titles.add(title)
            sources.append(title)

        if len(sources) == 3:
            break

    return answer, sources
    #print(response)
    #print(sources)

#rag_engine("What is Immigration Act?")


