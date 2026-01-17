from langchain_ollama import OllamaLLM

def expiry_agent(expiring, dietary_preference='both'):
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")
    
    dietary_rules = {
        'veg': 'VEGETARIAN ONLY',
        'non-veg': 'NON-VEGETARIAN',
        'both': 'FLEXIBLE'
    }
    
    prompt = f"""You are a food expiry analysis agent.
Dietary Preference: {dietary_rules.get(dietary_preference, 'FLEXIBLE')}

These ingredients are expiring soon: {', '.join(expiring)}

For each:
1. What problems occur if unused?
2. Which to consume first?
3. How to use them in {dietary_rules.get(dietary_preference, 'FLEXIBLE').lower()} cooking?

Keep it brief and practical."""
    
    return llm.invoke(prompt)
