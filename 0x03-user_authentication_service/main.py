#!/usr/bin/env python3
"""
Testing module for user authentication and management app.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user.
    """
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, f"Failed to register user: {
        response.text}"
    payload = response.json()
    assert payload == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with an incorrect password.
    """
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401, f"Unexpected status code: {
        response.status_code}"


def log_in(email: str, password: str) -> str:
    """
    Log in a user with correct credentials.
    """
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200, f"Failed to log in: {response.text}"
    payload = response.json()
    assert payload == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Attempt to access the profile endpoint without being logged in.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Unexpected status code: {
        response.status_code}"


def profile_logged(session_id: str) -> None:
    """
    Access the profile endpoint while logged in.
    """
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200, f"Failed to access profile: {
        response.text}"
    payload = response.json()
    assert "email" in payload, "Missing email in profile payload"


def log_out(session_id: str) -> None:
    """
    Log out the user by invalidating the session.
    """
    response = requests.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id})
    assert response.status_code == 302, f"Failed to log out: {
        response.status_code}"


def reset_password_token(email: str) -> str:
    """
    Generate a reset password token for the user.
    """
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"Failed to generate reset token: {
        response.text}"
    payload = response.json()
    assert "reset_token" in payload, "Missing reset token in response"
    return payload["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the user's password using a reset token.
    """
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password},
    )
    assert response.status_code == 200, f"Failed to update password: {
        response.text}"
    payload = response.json()
    assert payload == {"email": email, "message": "Password updated"}


# Test Workflow
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
