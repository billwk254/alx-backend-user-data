#!/usr/bin/env python3
"""
Definition of SessionDBAuth class
"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth Class.

    This class extends SessionExpAuth and implements session
    management with database persistence.
    """

    def create_session(self, user_id=None):
        """
        Create a Session ID for a given user ID and persist it in the database.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated session ID, or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a given session ID from the database.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID, or None if not found.
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """
        Destroy a UserSession instance based on a session ID from a request cookie.

        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
