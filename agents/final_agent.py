from langchain_ollama import OllamaLLM
from utils.grocery_tool import grocery_tool


def extract_missing_items(text):
    common_items = [
        "tomato", "onion", "potato", "milk",
        "bread", "egg", "rice", "oil", "cheese"
    ]

    found = []
    text_lower = text.lower()

    for item in common_items:
        if item in text_lower:
            found.append(item)

    return found


def final_agent(plan, audit, dietary_preference='both'):
    llm = OllamaLLM(
        model="mistral",
        base_url="http://localhost:11434"
    )

    dietary_label = {
        'veg': 'Vegetarian',
        'non-veg': 'Non-Vegetarian',
        'both': 'Flexible (Vegetarian + Non-Vegetarian)'
    }

    missing_items = extract_missing_items(plan + audit)

    grocery_data = grocery_tool(missing_items)

    prompt = f"""
You are ZeroBite Final Decision Agent.

Dietary Preference: {dietary_label.get(dietary_preference)}

Meal Plan:
{plan}

Waste Audit:
{audit}

Missing Ingredients:
{missing_items}

Quick-commerce tool response (Zepto simulation):
{grocery_data}

Your tasks:
1. Decide whether buying is NECESSARY or AVOIDABLE
2. Provide minimal shopping list
3. Create a 2-day meal schedule
4. Estimate waste reduction %
5. Mention dietary compliance

Prioritize waste reduction over convenience.
Keep response short and practical.
"""

    response = llm.invoke(prompt)

    return {
        "ai_response": response,
        "tool_used": "Zepto (simulated)",
        "missing_items": missing_items,
        "grocery": grocery_data
    }
