#!/usr/bin/env python3
"""Module for Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Retrieve the status of the API.

    Returns:
        JSON response indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Retrieve statistics about the number of objects.

    Returns:
        JSON response containing statistics about the number of objects.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """GET /api/v1/unauthorized
    Simulate an unauthorized error.

    Returns:
        None. Aborts with a 401 error.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """GET /api/v1/Forbidden
    Simulate a forbidden error.

    Returns:
        None. Aborts with a 403 error.
    """
    abort(403)
