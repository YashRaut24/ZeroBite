from langchain_ollama import OllamaLLM

def planner_agent(ingredients, expiring, dietary_preference='both'):
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")
    
    dietary_rules = {
        'veg': 'VEGETARIAN ONLY - Do NOT suggest eggs, chicken, fish, meat, or any animal products.',
        'non-veg': 'NON-VEGETARIAN - You may suggest meat, chicken, fish, eggs, and all animal products.',
        'both': 'FLEXIBLE - You may suggest vegetarian or non-vegetarian recipes based on available ingredients.'
    }
    
    prompt = f"""You are a food waste reduction planning agent.

DIETARY PREFERENCE: {dietary_rules.get(dietary_preference, dietary_rules['both'])}

Available ingredients: {ingredients}
Expiring soon: {expiring}

Provide a brief plan:
1. The problem
2. The goal
3. Key tasks to reduce waste

Remember: Follow the dietary preference strictly. Keep it concise."""
    
    return llm.invoke(prompt)
