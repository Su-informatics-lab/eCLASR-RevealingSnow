import datetime
import json

from flask import Response


# Adapted from https://stackoverflow.com/a/22238613/228591
def _json_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return "{:04d}-{:02d}-{:02d}".format(obj.year, obj.month, obj.day)

    raise TypeError("Type {} not serializable".format(type(obj)))


def jsonify(context):
    return json.dumps(context, default=_json_serializer)


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
