import os
import glob
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from dotenv import load_dotenv

load_dotenv(override=True)

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_INDEX_NAME = "langchain-chunks-index"
PINECONE_NAMESPACE = "personal"

KNOWLEDGE_BASE = str(Path(__file__).parent / "knowledge-base")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def fetch_documents():
    folders = glob.glob(str(Path(KNOWLEDGE_BASE) / "*"))
    documents = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(
            folder, glob="**/*.md", 
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        folder_docs = loader.load()
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    return documents

def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks

def get_pinecone_index():
    pinecone = Pinecone(api_key=PINECONE_API_KEY)

    if not pinecone.has_index(PINECONE_INDEX_NAME):
        pinecone.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    return pinecone.Index(PINECONE_INDEX_NAME)

def create_embeddings(chunks):
    index = get_pinecone_index()

    stats = index.describe_index_stats()
    if PINECONE_NAMESPACE in stats.namespaces:
        index.delete(delete_all=True, namespace=PINECONE_NAMESPACE)

    vectorstore = PineconeVectorStore(
        embedding=embeddings,
        index=index,
        namespace=PINECONE_NAMESPACE,
    )

    vectorstore.add_documents(documents=chunks)

    print("successfully loaded chunks")

if __name__ == "__main__":
    documents = fetch_documents()
    chunks = create_chunks(documents)
    create_embeddings(chunks)
    print("Ingestion complete")


