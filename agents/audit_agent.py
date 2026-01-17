from langchain_ollama import OllamaLLM

def audit_agent(meal_plan, ingredients, dietary_preference='both'):
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")
    
    dietary_label = {
        'veg': '(Vegetarian)',
        'non-veg': '(Non-Vegetarian)',
        'both': '(Flexible)'
    }
    
    prompt = f"""You are a food audit agent.
Dietary Mode: {dietary_label.get(dietary_preference, '(Flexible)')}

Meal plan proposed:
{meal_plan}

Current ingredients: {ingredients}

Audit:
1. Can these meals be made?
2. What essential items are missing?
3. Are all recipes compliant with the dietary preference?

Keep it brief."""
    
    return llm.invoke(prompt)
