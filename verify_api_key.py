"""
Verification script to test Google Gemini API key configuration
Tests all components: Gemini LLM, Embeddings, and Vector Store
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("GOOGLE GEMINI API KEY VERIFICATION")
print("=" * 60)

# Check 1: API Key exists
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("\n❌ FAILED: GOOGLE_API_KEY not found in .env file")
    print("   Create a .env file in root with: GOOGLE_API_KEY=your_key_here")
    exit(1)

print("\n✅ API Key found (length: {} chars)".format(len(api_key)))
print("   First 10 chars: {}...".format(api_key[:10]))

# Check 2: Test Gemini LLM
print("\n" + "-" * 60)
print("Testing Gemini LLM Connection...")
print("-" * 60)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key
    )
    
    response = llm.invoke("Say 'Hello from Gemini!' in one sentence")
    print("✅ LLM Connection: SUCCESS")
    print("   Response: {}".format(response.content[:80]))
except Exception as e:
    print("❌ LLM Connection: FAILED")
    print("   Error: {}".format(str(e)))
    exit(1)

# Check 3: Test Embeddings (for Vector Store)
print("\n" + "-" * 60)
print("Testing Google Embeddings...")
print("-" * 60)
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    
    test_embedding = embeddings.embed_query("test ingredient")
    print("✅ Embeddings: SUCCESS")
    print("   Embedding dimension: {} dimensions".format(len(test_embedding)))
except Exception as e:
    print("❌ Embeddings: FAILED")
    print("   Error: {}".format(str(e)))
    exit(1)

# Check 4: Test Vector Store
print("\n" + "-" * 60)
print("Testing Vector Store Connection...")
print("-" * 60)
try:
    from app.memory.vector_store import load_vector_store
    
    vector_db = load_vector_store()
    test_search = vector_db.similarity_search("chicken recipe", k=1)
    print("✅ Vector Store: SUCCESS")
    print("   Found {} documents".format(len(test_search)))
except Exception as e:
    print("❌ Vector Store: FAILED")
    print("   Error: {}".format(str(e)))
    exit(1)

# Final summary
print("\n" + "=" * 60)
print("✅ ALL CHECKS PASSED - System is ready to use!")
print("=" * 60)
print("\nYour API key is properly configured for:")
print("  ✓ Expiry Agent")
print("  ✓ Meal Agent")
print("  ✓ Audit Agent")
print("  ✓ Vector Store (Recipe Search)")