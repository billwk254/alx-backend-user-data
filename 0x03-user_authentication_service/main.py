#!/usr/bin/env python3
"""
End-to-End Integration Testing Script
"""

import requests

# Base URL for API requests
DOMAIN = "http://0.0.0.0:5000/%s"

def register_user(email: str, password: str) -> None:
    """Test user registration endpoint."""
    url = DOMAIN % "users"
    payload = [("email", email), ("password", password)]
    expected = {"email": email, "message": "User created"}
    
    # Test registration with valid credentials
    res = requests.post(url, data=payload)
    assert res.status_code == 200
    assert res.json() == expected

    # Test registration with already registered email
    expected = {"message": "Email already registered"}
    res = requests.post(url, data=payload)
    assert res.status_code == 400
    assert res.json() == expected

def log_in_wrong_password(email: str, password: str) -> None:
    """Test login endpoint with incorrect password."""
    url = DOMAIN % "sessions"
    payload = [("email", email), ("password", password)]
    expected = {"error": "Unauthorized"}
    
    # Test login with incorrect password
    res = requests.post(url, data=payload)
    assert res.status_code == 401
    assert res.json() == expected
    assert res.cookies == {}

def profile_unlogged() -> None:
    """Test profile route with unlogged user."""
    url = DOMAIN % "profile"
    expected = {"error": "Forbidden"}
    
    # Test accessing profile without session
    res = requests.get(url, cookies=dict())
    assert res.status_code == 403
    assert res.json() == expected

def log_in(email: str, password: str) -> str:
    """Test login with valid credentials and return session ID."""
    url = DOMAIN % "sessions"
    payload = [("email", email), ("password", password)]
    expected = {"email": email, "message": "Logged in"}
    
    # Test login with valid credentials
    res = requests.post(url, data=payload)
    assert res.status_code == 200
    assert res.json() == expected
    
    # Return session ID
    return res.cookies.get("session_id", None)

def profile_logged(session_id: str) -> None:
    """Test profile route for a valid logged-in user."""
    url = DOMAIN % "profile"
    
    # Test accessing profile with session ID
    res = requests.get(url, cookies=dict(session_id=session_id))
    assert res.status_code == 200
    assert res.json().get("email") is not None

def log_out(session_id: str) -> None:
    """Test logout route."""
    url = DOMAIN % "sessions"
    
    # Test logout with session ID
    res = requests.delete(url, cookies=dict(session_id=session_id))
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome"}

def reset_password_token(email: str) -> str:
    """Test reset password token route and return reset token."""
    url = DOMAIN % "reset_password"
    
    # Test getting reset token
    res = requests.post(url, data={"email": email})
    assert res.status_code == 200
    reset_token = res.json().get("reset_token")
    assert isinstance(reset_token, str)
    assert len(reset_token) > 0
    
    # Return reset token
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test password update route."""
    url = DOMAIN % "reset_password"
    payload = [
        ("email", email),
        ("reset_token", reset_token), ("new_password", new_password)]
    expected = {"email": email, "message": "Password updated"}
    
    # Test updating password
    res = requests.put(url, data=payload)
    assert res.status_code == 200
    assert res.json() == expected

# Test data
EMAIL = "guillaume@holberton.io"
PASSWORD = "b4l0u"
NEW_PASSWORD = "t4rt1fl3tt3"

if __name__ == "__main__":
    # Run tests
    register_user(EMAIL, PASSWORD)
    log_in_wrong_password(EMAIL, NEW_PASSWORD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWORD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWORD)
    log_in(EMAIL, NEW_PASSWORD)
