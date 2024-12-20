#!/usr/bin/env python3
"""
Auth module for password hashing.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password string using bcrypt.

    Returns:
        bytes: The salted hash of the input password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
