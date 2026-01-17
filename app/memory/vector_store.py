from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.embeddings import Embeddings
import os
import hashlib

class SimpleEmbeddings(Embeddings):
    """Fallback embeddings for testing when Google API fails"""
    
    def embed_documents(self, texts):
        """Generate simple hash-based embeddings"""
        return [[float(ord(c)) / 255.0 for c in hashlib.md5(text.encode()).hexdigest()[:20]] for text in texts]
    
    def embed_query(self, text):
        """Generate simple hash-based embedding for query"""
        return [float(ord(c)) / 255.0 for c in hashlib.md5(text.encode()).hexdigest()[:20]]

def load_vector_store():
    try:
        # Try Google API embeddings first
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        print("✓ Using Google Generative AI Embeddings")
    except Exception as e:
        print(f"⚠️ Google Embeddings failed: {e}")
        print("✓ Falling back to simple hash-based embeddings")
        embeddings = SimpleEmbeddings()

    texts = []
    with open("data/recipes.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:  # Only add non-empty lines
                texts.append(line)

    if not texts:
        raise ValueError("No recipes found in data/recipes.txt")

    return Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
