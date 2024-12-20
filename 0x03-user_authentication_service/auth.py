#!/usr/bin/env python3
"""
Auth module for password hashing and user registration
"""

from typing import Union, Optional
from user import User
from db import DB
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Hash a password string using bcrypt.

    Returns:
        bytes: The salted hash of the input password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """
    Generate a new UUID as a string.

    Returns:
        str: A string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the provided email and password.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.

        Returns:
            bool: True if login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a session ID for a user identified by their email.

        Returns:
            str: The session ID if the user exists, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)

        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self,
                                 session_id: Optional[str]) -> Optional[User]:
        """
        Get a user from a given session ID.

        Returns:
            User: The user corresponding to the session ID, or None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session by setting their session_id to None.

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a password reset token for a user.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)

            reset_token = self._generate_uuid()

            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token
        except NoResultFound:
            raise ValueError(f"User with email {email} does not exist")
