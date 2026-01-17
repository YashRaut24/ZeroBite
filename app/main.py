from fastapi import FastAPI
from dotenv import load_dotenv
from app.schemas.food import PlannerInput
from app.services.planner_flow import run_zero_bite_planner

load_dotenv()

app = FastAPI(title="ZeroBite")

@app.get("/")
def root():
    return {"message": "Welcome to ZeroBite API", "docs": "/docs"}

@app.post("/plan")
def generate_plan(data: PlannerInput):
    print(data)
    return run_zero_bite_planner(data)
