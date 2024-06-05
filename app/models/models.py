from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.db import Base
from enums.enums import Role

class User (Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    role = Column(Enum(Role), default=Role.user)

    orders_placed = relationship("Order", back_populates="customer", foreign_keys="[Order.user_id]")
    orders_taken = relationship("Order", back_populates="waiter", foreign_keys="[Order.waiter_id]")


class Meals(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key= True, index=True)
    title = Column(String, index= True)
    category = Column(String)
    description = Column(String)
    price = Column(Float)

    order_details = relationship("OrderDetail", back_populates="meal")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    waiter_id = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Integer, default=1)

    in_process = Column(Boolean, default=True)
    
    customer = relationship("User", back_populates="orders_placed", foreign_keys=[user_id])
    waiter = relationship("User", back_populates="orders_taken", foreign_keys=[waiter_id])
    order_details = relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    meal_id = Column(Integer, ForeignKey("meals.id"))
    quantity = Column(Integer, default=1)

    # Relationships
    order = relationship("Order", back_populates="order_details")
    meal = relationship("Meals", back_populates="order_details")

