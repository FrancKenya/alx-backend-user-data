#!/usr/bin/env python3
"""SQLAlchemy model for the 'users' table."""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """SQLAlchemy model for the 'users' table."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)


if __name__ == "__main__":
    engine = create_engine('sqlite:///auth_service.db')
    Base.metadata.create_all(engine)
    print("Database and 'users' table created!")
