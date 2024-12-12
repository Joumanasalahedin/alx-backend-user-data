#!/usr/bin/env python3
"""
Module for securely hashing passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a random salt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: A salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
