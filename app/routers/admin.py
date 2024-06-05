from fastapi import APIRouter, Depends, HTTPException, status
from schemes.user_schema import CreateUser
from security.security import get_current_user_role
from database.db import get_db
from enums.enums import Role
from sqlalchemy.orm import Session
from utils import utils
from models import models
from crud.cruds import create_user, get_meals, get_product_details_by_id, explore_users



router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.post("/createWaiter")
async def create_waiter_profile(waiter: CreateUser, role:Role, db: Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.admin))):
    print(user)
    if user is None:
        raise utils.get_user_exception
    
    db_waiter = db.query(models.User).filter(models.User.email == waiter.email)

    if db_waiter is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="waiter with this email have already exists"
        )
    
    new_waiter = create_user(waiter, role, db)

    return new_waiter

# @router.put("/updateUserDetails/{id}")
# async def update_user_details(id:int, )

@router.get("/explore")
async def explore_meals(skip:int = 0, limit:int = 10, db:Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.admin))):
    return get_meals(limit=limit, skip=skip, db=db)

@router.get("/mealDetail/{id}")
async def get_meal_details_by_id(id:int, db:Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.admin))):
    if user is None:
        raise utils.get_user_exception
    
    return get_product_details_by_id(id, db)

@router.get("/exploreUsers")
async def explore_users(skip:int = 0, limit:int = 10, db:Session = Depends(get_db), user:dict = Depends(get_current_user_role(Role.admin))):
    if user is None :
        raise utils.get_user_exception
    
    return explore_users(skip, limit, db)

# @router.post("/createMeal")
# async def create_meal():



