from pydantic import BaseModel, Field
from typing import List
from typing import Optional

class MealOrder(BaseModel):
    meal_id: int
    quantity: int

class OrderRequest(BaseModel):
    waiterid: int
    meals: List[MealOrder]

class CreateMeal(BaseModel):

    title : Field(str, max_length=100, min_length=3)
    category : Field(str, max_length=100, min_length=5)
    description = Field(str, max_length=100, min_length=5)
    price = float
    

class UpdateMeal(BaseModel):

    title: Optional[str]
    category : Optional[str]
    description = Optional[str]
    price = Optional[str]
