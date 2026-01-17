from langchain_ollama import OllamaLLM

def final_agent(plan, audit, dietary_preference='both'):
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")
    
    dietary_label = {
        'veg': 'Vegetarian',
        'non-veg': 'Non-Vegetarian',
        'both': 'Flexible (Vegetarian + Non-Vegetarian)'
    }
    
    prompt = f"""You are a final recommendation agent.
Dietary Preference: {dietary_label.get(dietary_preference, 'Flexible')}

Based on this plan:
{plan}

And audit:
{audit}

Provide final recommendations:
1. Shopping list (minimal items needed)
2. 2-day meal schedule
3. Estimated waste reduction %
4. Dietary compliance note

Keep it concise and actionable."""
    
    return llm.invoke(prompt)
