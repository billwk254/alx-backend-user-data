#!/usr/bin/env python3
""" UserSession Module """

from models.base import Base

class UserSession(Base):
    """
    UserSession Class.

    This class represents a user session, extending the Base model.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession instance.

        Args:
            *args (list): Positional arguments.
            **kwargs (dict): Keyword arguments.

        Keyword Args:
            user_id (str): The ID of the associated user.
            session_id (str): The ID of the session.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
