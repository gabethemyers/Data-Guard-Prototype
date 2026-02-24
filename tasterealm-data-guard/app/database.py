import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://gabriel:devpassword123@localhost:5432/tasterealm_dev",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
