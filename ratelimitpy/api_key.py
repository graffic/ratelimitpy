"""
Handles the api_key attribute in the flask g context object
"""
from functools import wraps
from flask import g, abort, request


def require_api_key(original):
    """Decorator for flask view that will fail if no key available"""
    @wraps(original)
    def wrapped(*args, **argv):
        if g.api_key is None:
            abort(401)
        return original(*args, **argv)
    return wrapped


def set_api_key():
    """Sets the api_key attribute in g using Authorization header"""
    auth = request.headers.get("Authorization", "")
    parts = auth.split(" ")
    if len(parts) != 2:
        g.api_key = None
    else:
        g.api_key = parts[1]
