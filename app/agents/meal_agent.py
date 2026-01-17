from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os

llm = None
prompt = None

def _init_llm():
    global llm, prompt
    if llm is None:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        prompt = PromptTemplate(
            input_variables=["urgent_items", "pantry", "recipes"],
            template="""
You are a meal planning agent.

Urgent ingredients:
{urgent_items}

Pantry:
{pantry}

Known recipes:
{recipes}

Create a 2-day meal plan minimizing waste.
Also give minimal shopping list.
"""
        )

def run_meal_agent(urgent_items, pantry, recipes):
    _init_llm()
    return llm.invoke(
        prompt.format(
            urgent_items=urgent_items,
            pantry=", ".join(pantry),
            recipes=recipes
        )
    ).content
