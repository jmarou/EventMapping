import os
from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

db_path = os.path.join(os.path.dirname(__file__), "tweets.db")
SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(db_path)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def db_session() -> ContextManager[Session]:
    """Returns a context manager to do crud database operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
