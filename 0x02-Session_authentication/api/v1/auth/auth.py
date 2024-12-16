#!/usr/bin/env python3
"""
Authentication module.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        # Ensure path has a trailing slash for comparison
        path = path.rstrip("/") + "/"

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if path == excluded_path.rstrip('/') + '/':
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from a Flask request object.

        Returns:
            str: None for now.
        """
        if request is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        Retrieves the current user based on a Flask request object.

        Returns:
            TypeVar('User'): None for now.
        """
        return None
