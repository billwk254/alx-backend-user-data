#!/usr/bin/env python3
"""Module containing routes for handling API status and errors."""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Endpoint to retrieve the status of the API.

    Returns:
        JSON response indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Endpoint to retrieve statistics about objects.

    Returns:
        JSON response containing statistics about the objects.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """Endpoint to simulate an unauthorized error.

    Returns:
        None. Aborts with a 401 error.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """Endpoint to simulate a forbidden error.

    Returns:
        None. Aborts with a 403 error.
    """
    abort(403)
