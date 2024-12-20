#!/usr/bin/env python3
"""
Auth module for password hashing and user registration
"""

from typing import Optional
from user import User
from db import DB
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash a password string using bcrypt.

    Returns:
        bytes: The salted hash of the input password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


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