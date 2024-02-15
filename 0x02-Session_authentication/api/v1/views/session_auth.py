#!/usr/bin/env python3
"""
Session Authentication Route Handlers
"""

from werkzeug import exceptions
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request
from os import abort, environ, getenv

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """
    Handle User Login via Session.

    This route handles user login via session authentication.
    It expects an email and password in the request form data.

    Returns:
        str: JSON response containing the user instance if login is successful,
             along with a session cookie. Returns appropriate error messages
             with corresponding HTTP status codes if any data is missing or if
             authentication fails.
    """
    user_email = request.form.get('email', None)
    user_password = request.form.get('password', None)

    if user_email is None or user_email == "":
        return jsonify({"error": "email missing"}), 400
    if user_password is None or user_password == "":
        return jsonify({"error": "password missing"}), 400

    is_valid_user = User.search({'email': user_email})

    if not is_valid_user:
        return jsonify({"error": "no user found for this email"}), 404

    is_valid_user = is_valid_user[0]

    if not is_valid_user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(is_valid_user.id)
    cookie_response = getenv('SESSION_NAME')
    user_dict = jsonify(is_valid_user.to_json())

    user_dict.set_cookie(cookie_response, session_id)
    return user_dict

@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False)
def session_logout() -> str:
    """
    Handle User Logout via Session.

    This route handles user logout via session authentication.
    It deletes the user session, effectively logging the user out.

    Returns:
        str: Empty JSON response with a 200 status code if logout is successful.
             Returns a 404 status code if logout fails.
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
