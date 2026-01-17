from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.schemas.food import PlannerInput
from app.services.planner_flow import run_zero_bite_planner

load_dotenv()

app = FastAPI(title="ZeroBite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to ZeroBite API", "docs": "/docs"}

@app.post("/plan")
def generate_plan(data: PlannerInput):
    try:
        result = run_zero_bite_planner(data)
        return result
    except Exception as e:
        print(f"ERROR in /plan: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "expiry_analysis": "Error processing request",
            "meal_plan": str(e),
            "audit_report": f"Backend error: {str(e)}"
        }
