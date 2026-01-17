from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    texts = []
    with open("data/recipes.txt", "r") as f:
        for line in f:
            texts.append(line.strip())

    return Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
