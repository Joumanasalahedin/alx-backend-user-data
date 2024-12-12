#!/usr/bin/env python3
"""
BasicAuth module.
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header.

        Returns:
            str: The Base64 part of the Authorization header, None if invalid.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_header: str) -> str:
        """
        Decodes a Base64 string.

        Returns:
            str: The decoded value as a UTF-8 string, or None if invalid.
        """
        if base64_header is None:
            return None

        if not isinstance(base64_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_header: str) -> (str, str):
        """
        Extracts user email and password from a Base64 decoded string.

        Returns:
            tuple: (email, password) or (None, None) if invalid.
        """
        if decoded_base64_header is None:
            return None, None

        if not isinstance(decoded_base64_header, str):
            return None, None

        if ':' not in decoded_base64_header:
            return None, None

        email, password = decoded_base64_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a User instance based on email and password.

        Returns:
            User: The User instance if valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None
