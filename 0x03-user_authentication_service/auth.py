#!/usr/bin/env python3
"""
Authentication Module: Provides functionality for user authentication.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from db import DB, User


def _generate_uuid() -> str:
    """Generate UUID

    Generates a random UUID string.
    """
    from uuid import uuid4
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """Hash Password

    Encrypts a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Authentication Class

    Provides methods to interact with the authentication database.
    """
    def __init__(self):
        """Initialize Authentication

        Initializes the Auth class with a database instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register User

        Creates a new user if the email does not exist in the database.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError("User %s already exists" % email)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate Login

        Validates login credentials against the database.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """Create Session

        Generates a session ID for a user and updates the database.
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pass
        else:
            try:
                self._db.update_user(user.id, session_id=session_id)
            except (NoResultFound, ValueError):
                pass
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get User from Session ID

        Retrieves user information from the database using the session ID.
        """
        if session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                pass
        return None

    def destroy_session(self, user_id: str) -> None:
        """Destroy Session

        Removes session ID from the database for a given user.
        """
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get Reset Password Token

        Generates a password reset token and updates the database.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        try:
            self._db.update_user(user.id, reset_token=reset_token)
        except (NoResultFound, ValueError):
            raise ValueError
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update Password

        Updates the user's password using the reset token.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=password, reset_token=None)
        except NoResultFound:
            raise ValueError
        return None
