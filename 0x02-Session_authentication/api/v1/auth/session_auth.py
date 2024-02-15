#!/usr/bin/env python3
"""
Session Authentication Module
"""

from typing import Dict
from flask.globals import session
from api.v1.auth.auth import Auth
from models.user import User
import uuid

class SessionAuth(Auth):
    """
    Session Authentication Class.

    This class inherits from the Auth class and provides methods
    for managing user sessions through session IDs.
    """

    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create Session.

        Generates a session ID and associates it with the provided user ID.

        Args:
            user_id (str): The ID of the user to associate with the session.

        Returns:
            str: The generated session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get User ID for Session ID.

        Retrieves the user ID associated with the given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID, or None if not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        Get Current User.

        Retrieves the current user based on the session information in the request.

        Args:
            request: Optional Flask request object.

        Returns:
            User: The current user object, or None if not found.
        """
        cookie = self.session_cookie(request)
        session_user_id = self.user_id_for_session_id(cookie)
        user = User.get(session_user_id)
        return user

    def destroy_session(self, request=None):
        """
        Destroy Session.

        Deletes the session associated with the request, effectively logging out the user.

        Args:
            request: Optional Flask request object.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        cookie_data = self.session_cookie(request)
        if cookie_data is None:
            return False
        if not self.user_id_for_session_id(cookie_data):
            return False
        del self.user_id_by_session_id[cookie_data]
        return True
