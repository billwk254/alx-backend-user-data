#!/usr/bin/env python3
"""Authentication module."""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Class for handling authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path.

        Args:
            path: The path to be checked for authentication requirement.
            excluded_paths: List of paths that are excluded from authentication.

        Returns:
            True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request.

        Args:
            request: Flask request object.

        Returns:
            The value of the Authorization header if present, else None.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the current user from the request.

        Args:
            request: Flask request object.

        Returns:
            User object if authenticated, else None.
        """
        return None
