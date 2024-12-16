#!/usr/bin/env python3
"""
Session Authentication View Module
"""
from flask import request, jsonify, abort
from models.user import User
from os import getenv
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles POST /auth_session/login to log in a user via session authentication.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    users = User.search({"email": email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session for the user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Return the user's JSON representation and set the session cookie
    response = jsonify(user.to_json())
    cookie_name = getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(cookie_name, session_id)

    return response
