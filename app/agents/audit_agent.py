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
            input_variables=["plan", "ingredients"],
            template="""
You are a food waste auditor.

Ingredients:
{ingredients}

Meal Plan:
{plan}

Check if any ingredient may go unused.
Give waste risk level and suggestion.
"""
        )

def run_audit_agent(plan, ingredients):
    _init_llm()
    items = ", ".join([i.name for i in ingredients])
    return llm.invoke(
        prompt.format(plan=plan, ingredients=items)
    ).content
