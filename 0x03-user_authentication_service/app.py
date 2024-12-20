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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
