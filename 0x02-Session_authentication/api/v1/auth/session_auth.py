#!/usr/bin/env python3
"""
Session Authentication Module
"""
from api.v1.auth.auth import Auth
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
