import json

from flask import Response, request
from types import BooleanType


def json_requested():
    """Check if json is the preferred output format for the request."""
    best = request.accept_mimetypes.best_match(
        ['application/json', 'text/html'])
    return (best == 'application/json' and
            request.accept_mimetypes[best] >
            request.accept_mimetypes['text/html'])


def jsonify(obj):
    """Dump an object to JSON and create a Response object from the dump.
    Unlike Flask's native implementation, this works on lists.
    """
    dump = json.dumps(obj)
    return Response(dump, mimetype='application/json')


def truthiness(s):
    """Returns a boolean from a string"""
    if isinstance(s, BooleanType):
        return s

    if str(s).lower().startswith(('t', '1')):
        return True

    return False
