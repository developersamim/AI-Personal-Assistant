from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document
from langchain_ollama import ChatOllama

MODEL = "gpt-oss:20b"
OLLAMA_BASE_URL = "http://localhost:11434"
DB_NAME = str(Path(__file__).parent / "vector_db")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
RETRIEVAL_K = 10

SYSTEM_PROMPT = """
You are a knowledgeable, friendly assistant representing the personal assistant of Samim Ahmed.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
retriever = vectorstore.as_retriever()
llm = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model=MODEL,
    temperature=0
    )

def fetch_context(question: str) -> list[Document]:
    """
    Retrieve relevant context documents for a question.
    """
    return retriever.invoke(question, k=RETRIEVAL_K)

def combined_question(question: str, history: list[dict] = []) -> str:
    """
    Combine all the user's messages into a single string.
    """
    prior = "\n".join(h["content"] for h in history if h["role"] == "user")
    return prior + "\n" + question

def answer_question(question: str, history: list[dict] = []) -> tuple[str, list[Document]]:
    """
    Answer the given question with RAG; return the answer and the context documents.
    """
    combined = combined_question(question, history)
    docs = fetch_context(combined)
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT.format(context=context)
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(convert_to_messages(history))
    messages.append(HumanMessage(content=question))
    response = llm.invoke(messages)
    return response.content, docs
    