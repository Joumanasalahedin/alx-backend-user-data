#!/usr/bin/env python3
"""
Basic Flask app for user registration.
"""

from flask import Flask, request, jsonify, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """
    Welcome route that returns a JSON payload.

    Returns:
        Response: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    Endpoint to register a new user.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    Endpoint to log in a user.
    Returns:
        - 200: JSON response with the user's email and a success message
        - 401: Error response if login information is incorrect.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(
        jsonify({"email": email, "message": "logged in"}), 200)
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Endpoint to log out a user.

    Returns:
        - 302: Redirects the user if the session is successfully destroyed.
        - 403: if the session ID is invalid or no user is found.
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/", code=302)


@app.route("/profile", methods=["GET"])
def profile():
    """
    Endpoint to retrieve a user's profile.

    Returns:
        - 200: JSON response with the user's email if the session is valid.
        - 403: Error if the session ID is invalid or the user does not exist.
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def reset_password():
    """
    Endpoint to generate a password reset token.

    Returns:
        - 200: user's email and the reset token if the email is registered.
        - 403: Error response if the email is not registered.
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    Endpoint to update a user's password.

    Returns:
        - 200: user's email and a success message if the password was updated.
        - 403: Error response if the reset token is invalid.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
