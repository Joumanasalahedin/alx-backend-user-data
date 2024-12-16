#!/usr/bin/env python3
"""
Session Authentication Module
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Session Authentication class that inherits from Auth.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a given user_id.
        Returns:
            str: The created Session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve a User ID based on a given Session ID.
        Returns:
            str: User ID corresponding to the session ID or None if invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieve a User instance based on a cookie value.
        Args:
            request: Flask request object.
        Returns:
            User: The User instance corresponding to the session ID, or None.
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)

        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        return User.get(user_id)
