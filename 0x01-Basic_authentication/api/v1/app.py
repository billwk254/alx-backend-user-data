#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine the authentication mechanism based on the AUTH_TYPE environment variable
auth_type = getenv('AUTH_TYPE', 'auth')
auth = None
if auth_type == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()

# Before request handler to perform authentication and authorization checks
@app.before_request
def before_request() -> str:
    """Handle before request"""
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if auth.require_auth(request.path, excluded_paths):
        auth_header = auth.authorization_header(request)
        user = auth.current_user(request)
        if auth_header is None:
            abort(401)
        if user is None:
            abort(403)

# Error handlers for 404, 401, and 403 status codes
@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403

# Run the application
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
