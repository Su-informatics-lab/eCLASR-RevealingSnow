import json

from flask import Response


def jsonify(context):
    return json.dumps(context)


def make_json_response(context, status=200, headers=None):
    if context is not None:
        context = jsonify(context)

    response = Response(
        context,
        status=status,
        headers=headers,
        mimetype='application/json'
    )

    return response
