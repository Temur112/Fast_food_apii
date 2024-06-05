from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_URL = "sqlite:///./fastfood.db"

engine = create_engine(
    DB_URL,connect_args={"checksame_thread": False}
)

SessionLocal = sessionmaker(autocommit=False ,autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()
        

