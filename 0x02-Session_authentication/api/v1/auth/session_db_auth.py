#!/usr/bin/env python3
"""
SessionDBAuth Module
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for session authentication stored in a database.
    """

    def create_session(self, user_id=None):
        """
        Create a session and store it in the database.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Create a new UserSession instance and save it
        user_session = UserSession(session_id=session_id, user_id=user_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a user ID based on a session ID stored in the database.
        """
        if session_id is None:
            return None

        # Search for the session in the database
        sessions = UserSession.search({"session_id": session_id})
        if not sessions or len(sessions) == 0:
            return None

        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id

        # Validate session expiration
        created_at = session.created_at
        if not created_at:
            return None

        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """
        Destroy a session stored in the database.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Search for and delete the session
        sessions = UserSession.search({"session_id": session_id})
        if not sessions or len(sessions) == 0:
            return False

        session = sessions[0]
        session.remove()
        return True
