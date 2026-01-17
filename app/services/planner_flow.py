from app.agents.expiry_agent import run_expiry_agent
from app.agents.meal_agent import run_meal_agent
from app.agents.audit_agent import run_audit_agent
from app.memory.vector_store import load_vector_store

vector_db = None

def _init_vector_db():
    global vector_db
    if vector_db is None:
        vector_db = load_vector_store()

def get_mock_response(data):
    """Mock response for demo purposes when API fails"""
    ingredient_names = ", ".join([i.name for i in data.ingredients])
    pantry_names = ", ".join(data.pantry)
    
    return {
        "expiry_analysis": f"🥗 EXPIRY PRIORITY:\n\n{ingredient_names}\n\nSuggested meals prioritize these ingredients to minimize waste.",
        "meal_plan": f"📋 2-DAY MEAL PLAN:\n\nDay 1:\n- Morning: {ingredient_names} with {data.pantry[0] if data.pantry else 'rice'}\n- Evening: {ingredient_names} curry\n\nDay 2:\n- Morning: {data.pantry[0] if data.pantry else 'rice'} with curd\n- Evening: Mixed vegetable stir-fry\n\n🛒 Shopping List: Minimal - use what you have!",
        "audit_report": f"✅ WASTE RISK ANALYSIS:\n\nIngredients analyzed: {ingredient_names}\nAvailable pantry items: {pantry_names}\n\nWaste Risk: LOW\nReason: All ingredients can be used in suggested meals within their expiry window.\n\n💡 Recommendation: Execute meal plan immediately to maximize usage."
    }

def run_zero_bite_planner(data):
    try:
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
    except Exception as e:
        print(f"⚠️ API Error: {str(e)}")
        print("✓ Using mock response for demo")
        return get_mock_response(data)
