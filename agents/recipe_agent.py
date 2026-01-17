from langchain_ollama import OllamaLLM

def recipe_agent(ingredients, expiring, dietary_preference='both'):
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")
    
    dietary_constraints = {
        'veg': 'STRICTLY VEGETARIAN - No meat, chicken, fish, or eggs',
        'non-veg': 'CAN INCLUDE - meat, chicken, fish, eggs, and animal products',
        'both': 'FLEXIBLE - vegetarian or non-vegetarian recipes'
    }
    
    prompt = f"""You are a meal planning agent.

DIETARY CONSTRAINT: {dietary_constraints.get(dietary_preference, dietary_constraints['both'])}
Available ingredients: {ingredients}
Priority (expiring): {expiring}

Suggest 4-5 simple meals that:
- Follow the dietary constraint STRICTLY
- Use expiring items first
- Are realistic to cook
- Minimize waste

List meals briefly."""
    
    return llm.invoke(prompt)
