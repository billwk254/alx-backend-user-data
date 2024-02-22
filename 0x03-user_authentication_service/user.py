#!/usr/bin/env python3
"""
User Authentication System: Defines the User class for authentication purposes.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


# Base class for ORM
Base = declarative_base()


class User(Base):
    """
    User class representing registered users in the authentication system.
    """
    __tablename__ = 'users'

    id = Column(Integer, autoincrement="auto", primary_key=True)
    email = Column(String(250), nullable=False)  # User's email address
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))  # Session ID for logged-in users
    reset_token = Column(String(250))  # Token used for password reset
