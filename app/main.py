from fastapi import FastAPI, Depends
from models import models
from database.db import engine
from routers import auth, waiter, user, admin


app = FastAPI()
models.Base.metadata.create_all(bind=engine)



app.include_router(auth.router)
app.include_router(waiter.router)
app.include_router(user.router)
app.include_router(admin.router)