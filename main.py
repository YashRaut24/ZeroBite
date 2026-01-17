from agents.planner_agent import planner_agent
from agents.expiry_agent import expiry_agent
from agents.recipe_agent import recipe_agent
from agents.audit_agent import audit_agent
from agents.final_agent import final_agent

ingredients = ["rice", "tomato", "onion", "curd"]
expiring = ["tomato", "curd"]

plan = planner_agent(ingredients, expiring)
expiry = expiry_agent(expiring)
meals = recipe_agent(ingredients, expiring)
audit = audit_agent(meals, ingredients)

final_output = final_agent(meals, audit)

print("🧠 PLAN\n", plan)
print("⏰ EXPIRY\n", expiry)
print("🍳 MEALS\n", meals)
print("🛒 AUDIT\n", audit)
print("✅ FINAL OUTPUT\n", final_output)
