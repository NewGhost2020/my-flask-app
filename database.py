from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///promotions.db')

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    return Session()


def close_session():
    Session.remove()
