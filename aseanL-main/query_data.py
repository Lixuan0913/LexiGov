import argparse
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
Answer the question based only on the following context.

Context:
{context}

Question:
{question}

Instructions:
- Write the answer in 3-5 bullet points.
- Use simple words that a 5th grade child can understand.
- Do not add information that is not in the context.
"""

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def rag_engine(query_text):

    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if(len(results) == 0 or results[0][1] < 0.4):
        print("Unable to find matching results.")
        return None, []
    
    context_text = "\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOllama(model="llama3")
    response = model.invoke(prompt)
    response_txt = response.content
    

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    #Testing
    #formatted_response = f"Response: {response_txt}\nSources: {sources}" 
    #print(formatted_response)
    
    return response_txt, sources



