from models.models import User, Meals, Order, OrderDetail
from schemes.user_schema import CreateUser
from sqlalchemy.orm import Session
from security.security import get_hashed_password
from enums.enums import Role
from schemes.order_meal_schema import CreateMeal, UpdateMeal



# User part
def create_user(user: CreateUser, role:Role, db: Session):
    new_user = User()

    new_user.email = user.email
    new_user.username = user.username
    new_user.role = role
    hashed_pass = get_hashed_password(user.password)
    new_user.password = hashed_pass

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_user.password = ""

    return new_user

def get_user_by_email(email:str, db: Session):
    return db.query(User).filter(User.email == email).first()

def get_product_details_by_id(id: int, db:Session):   #get_meal_details_by_id
    meal = db.query(Meals).filter(Meals.id == id).first()
    return meal

def get_meals(db:Session, skip, limit):
    return db.query(Meals).offset(skip).limit(limit).all()

def create_new_order(db:Session, waiterid:int, userid:int):
    new_order = Order()
    new_order.waiter_id = waiterid
    new_order.user_id = userid

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

def create_meal(meal:CreateMeal, db:Session):
    new_meal = Meals()
    new_meal.title = meal.title
    new_meal.description = meal.description
    new_meal.category = meal.category
    new_meal.price = meal.price

    # unique name constraint need to checked i fneeded (title)

    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return new_meal

def updatemeal(id:int, newmeal:UpdateMeal, db):
    meal = get_product_details_by_id(id, db)
    if newmeal.title:
        meal.title = newmeal.title

    if newmeal.description:
        meal.description = newmeal.description

    if newmeal.title:
        meal.category = newmeal.category

    if newmeal.price:
        meal.price = newmeal.price

    db.commit()
    db.refresh(meal)
    return meal

def delete_meal_by_id(id: int, db: Session):
    meal = get_product_details_by_id(id, db)
    if meal:
        db.delete(meal)
        db.commit()

    return meal

def get_order_by_id(id:int, db:Session):
    order = db.query(Order).filter(Order.id == id).first()
    order_details = db.query(OrderDetail).filter(OrderDetail.order_id == id).all()
    meal_details = []

    for detail in order_details:
        meal = db.query(Meals).filter(Meals.id == detail.meal_id).first()
        meal_details.append({
            "meal_id": meal.id,
            "title": meal.title,
            "quantity": detail.quantity,
            "price": meal.price
        })

    response = {
        "order_id": order.id,
        "user_id": order.user_id,
        "waiter_id": order.waiter_id,
        "in_process": order.in_process,
        "meals": meal_details
    }

    return response


##admin part

def explore_users(skip:int, limit:int, db:Session):
    return db.query(User).offset(skip).limit(limit).all()

## 
def calculate_waiting_time(db:Session, distance:int):
    meals = db.query(Order).filter(Order.in_process == True).all()
    estimated_time = 1.25 * len(meals) + 3 * distance
    return estimated_time
