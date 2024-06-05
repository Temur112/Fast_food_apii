from fastapi import APIRouter, Depends, HTTPException
from schemes.user_schema import CreateUser
from database.db import get_db
from sqlalchemy.orm import Session
from crud.cruds import get_user_by_email, create_default_user
from fastapi.security import OAuth2PasswordRequestForm
from security import security
from utils import utils


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401:{"user": "not authorized"}}

)

@router.post("/register")
async def register_user(newuser:CreateUser, db: Session = Depends(get_db)):
    user = get_user_by_email(newuser.email, db)

    if user is not None:
        raise HTTPException(status_code=400, detail="User with this email have already registered")
    
    new_user = create_default_user(newuser, db)

    return new_user

@router.post("/login")
async def genereate_token(formdata:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = security.authenticate_user(formdata.username, formdata.password, db)

    if not user:
        raise utils.token_exception
    
    token = security.create_access_token(user.email, user.id, user.role)

    return {
        "message": "Login successfull",
        "token": token
    }



