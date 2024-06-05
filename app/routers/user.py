from fastapi import APIRouter, Depends, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from security.security import get_current_user_role
from crud.cruds import get_meals, get_product_details_by_id
from enums.enums import Role
from schemes.order_meal_schema import MealOrder, OrderRequest
from utils import utils
from models import models
from crud.cruds import create_new_order, calculate_waiting_time



router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/explore")
async def explore_meals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    meals = get_meals(db, skip, limit)
    return meals

@router.get("/meals/{id}")
async def get_meal_detail_by_id(id: int, db:Session = Depends(get_db)):
    return get_meal_detail_by_id(id, db)

@router.post("/order")
async def oreder_meals(order_request: OrderRequest, distance:int = 1, db: Session = Depends(get_db), user: dict = Depends(get_current_user_role(Role.user))):
    if user is None:
        raise utils.get_user_exception
    
    waiter = db.query(models.User)\
        .filter(models.User.id == order_request.waiterid)\
        .filter(models.User.role == Role.waiter)\
        .first()
    
    if waiter is None:
        raise utils.no_such_waiter_exception
    
    new_order = create_new_order(db, order_request.waiterid, user.get("id"))
    

    for meal_in_order in order_request.meals:
        meal = db.query(models.Meals)\
            .filter(models.Meals.id == meal_in_order.meal_id)\
            .first()
        if not meal:
            raise HTTPException(status_code=404, detail=f"Meal with id {meal_in_order.meal_id} not found")

        order_detail = models.OrderDetail()
        order_detail.order_id = new_order.id
        order_detail.meal_id = meal_in_order.meal_id
        order_detail.quantity = meal_in_order.quantity

        db.add(order_detail)

    db.commit()

    waiting_time = calculate_waiting_time(db, distance)

    return {
        "status":"success",
        "order_id": new_order.id,
        "estimated_waiting_time": waiting_time
    }

