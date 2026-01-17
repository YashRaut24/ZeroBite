from app.agents.expiry_agent import run_expiry_agent
from app.agents.meal_agent import run_meal_agent
from app.agents.audit_agent import run_audit_agent
from app.memory.vector_store import load_vector_store

vector_db = None

def _init_vector_db():
    global vector_db
    if vector_db is None:
        vector_db = load_vector_store()

def run_zero_bite_planner(data):
    _init_vector_db()
    expiry_result = run_expiry_agent(data.ingredients)

    docs = vector_db.similarity_search(expiry_result, k=4)
    recipes = "\n".join([d.page_content for d in docs])

    meal_plan = run_meal_agent(
        expiry_result,
        data.pantry,
        recipes
    )

    audit = run_audit_agent(meal_plan, data.ingredients)

    return {
        "expiry_analysis": expiry_result,
        "meal_plan": meal_plan,
        "audit_report": audit
    }
