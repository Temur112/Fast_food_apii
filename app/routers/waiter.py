from fastapi import APIRouter, Depends, HTTPException, status
from database.db import get_db
from security.security import get_current_user_role
from sqlalchemy.orm import Session
from enums.enums import Role
from utils import utils
from models import models
from schemes.order_meal_schema import CreateMeal, UpdateMeal
from crud.cruds import create_meal, updatemeal, get_product_details_by_id, delete_meal_by_id, get_order_by_id



router = APIRouter(
    prefix="/waiter",
    tags=["waiter"]
)



@router.post("/createMeal")
async def create_meal(meal:CreateMeal, db:Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.waiter))):
    if user is None:
        raise utils.no_such_waiter_exception

    new_meal = create_meal(meal, db)

    return new_meal     


@router.put("/updateMeal/{id}")
async def update_meal(id: int, newmeal:UpdateMeal, db: Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.waiter))):
    if user is None:
        raise utils.no_such_waiter_exception
    
    meal = db.query(models.Meals).filter(models.Meals.id == id).first()

    if meal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )
    
    meal = updatemeal(id, newmeal, db)
    return meal

@router.delete("/deleteMeals/{id}")
async def delete_meal_by_id(id: int, db:Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.waiter))):
    if user is None:
        raise utils.no_such_waiter_exception
    
    meal = get_product_details_by_id(id, db)

    if meal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found meal")
    
    return delete_meal_by_id(id, db)



@router.get("/seeOrders")
async def explore_orders(id: int, db:Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.waiter))):
    if user is None:
        raise utils.no_such_waiter_exception
    
    order = db.query(models.Order).filter(models.Order.id == id).first()

    if order is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="no such order"
        )

    return get_order_by_id(id, db)

    



@router.put("/update/{order_id}/status")
async def update_order_status(order_id:int, in_proccess:bool, db:Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role))):
    if user is None:
        return utils.no_such_waiter_exception()
    
    order = db.query(models.Order.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order Not Found"
        )
    

    order.in_process = in_proccess
    
    db.commit()
    # db.refresh(order)
    return {"status": "success", "order_id": order.id, "in_process": order.in_process}


@router.get("/getmealsDetail/{id}")
async def get_meal_details(id:int, db: Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.waiter))):
    if user is None:
        raise utils.no_such_waiter_exception
    meal = db.quer(models.Meals).filter(models.Meals == id).first()
    if meal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )
    return get_product_details_by_id(id, db) #return meal



