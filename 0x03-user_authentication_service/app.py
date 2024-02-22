#!/usr/bin/env python3
"""
Flask Application for User Authentication.
"""


from flask import Flask, abort, jsonify, request, make_response, redirect
from auth import Auth

# Initialize the authentication module
AUTH = Auth()

# Create the Flask application
app = Flask(__name__)


# Error handler for 401 Unauthorized
@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handles unauthorized access"""
    return jsonify({"error": "Unauthorized"}), 401


# Error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden(error) -> str:
    """Handles forbidden access"""
    return jsonify({"error": "Forbidden"}), 403


# Home route
@app.route("/")
def home() -> str:
    """Displays a welcome message"""
    return jsonify({"message": "Welcome"})


# Register new users
@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """Registers a new user"""
    email, password = request.form.get('email'), request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "Email already registered"}), 400
    return jsonify({"email": email, "message": "User created"})


# Login route
@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Logs in a user and creates a session"""
    email, password = request.form.get('email'), request.form.get('password')
    if AUTH.valid_login(email=email, password=password):
        res = make_response(jsonify({"email": email, "message": "Logged in"}))
        res.set_cookie("session_id", AUTH.create_session(email))
        return res
    abort(401)


# Logout route
@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logs out a user"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


# Profile route
@app.route("/profile", strict_slashes=False)
def profile():
    """Displays user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


# Reset password route
@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Sends reset password token to user's email"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


# Update password route
@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Updates user's password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except Exception:
        pass
    abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
