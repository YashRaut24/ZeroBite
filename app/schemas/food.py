from pydantic import BaseModel
from typing import List

class Ingredient(BaseModel):
    name: str
    expiry_days: int

class PlannerInput(BaseModel):
    ingredients: List[Ingredient]
    pantry: List[str]
