#!/usr/bin/env python3
"""
Session Expiration Authentication Module
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for session expiration.
    """

    def __init__(self):
        """
        Initialize SessionExpAuth with session duration.
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a Session ID with an expiration time.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a User ID based on a session ID with expiration check.
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if not session_data:
            return None

        if "created_at" not in session_data:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        created_at = session_data.get("created_at")
        if not created_at or not isinstance(created_at, datetime):
            return None

        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session_data.get("user_id")
