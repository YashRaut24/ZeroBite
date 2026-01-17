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
            input_variables=["items"],
            template="""
You are a food expiry analyst.

Ingredients:
{items}

Return list of ingredients sorted by urgency.
Output as plain text list.
"""
        )

def run_expiry_agent(ingredients):
    _init_llm()
    items = "\n".join(
        [f"{i.name} expires in {i.expiry_days} days" for i in ingredients]
    )
    return llm.invoke(prompt.format(items=items)).content
