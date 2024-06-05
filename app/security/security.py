from passlib.context import CryptContext
from models.models import User
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from utils import utils
from jose.exceptions import  JWTError


ALGORITHM = "HS256"
SECRETKEY = "fXbEkPUG5G5ejbOHjddtWs4Dei3rW-7BuHScRrJmL5c"



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plaintext:str, hashedpassword:str):
    return pwd_context.verify(plaintext, hashedpassword)


def authenticate_user(email:str, password:str, db):
    user = db.query(User)\
        .filter(User.email == email)\
        .first()
    
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user


def create_access_token(email:str, userid:int, role, expires_delta: Optional[timedelta] = None):
    encode = {
        "login": email,
        "id": userid,
        "role": role
    }


    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    encode.update({"expires": expire.isoformat()})

    return jwt.encode(encode, SECRETKEY, ALGORITHM)


oauth2bearer = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token:str = Depends(oauth2bearer)):
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=[ALGORITHM])
        login = payload.get("email")
        userid = payload.get("id")
        role = payload.get("role")

        if login is None or userid is None:
            raise utils.get_user_exception()
        
        return {
            "id":userid,
            "login": login,
            "role": role 
        }
    
    except JWTError:
        raise  utils.get_user_exception
    

async def get_current_user_role(required_role:str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user.get("role") != required_role:
            raise utils.permission_exception
        
        return user
    return role_checker