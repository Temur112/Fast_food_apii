from fastapi import FastAPI
from models import models
from database.db import engine
from routers import auth, waiter

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(waiter.router)