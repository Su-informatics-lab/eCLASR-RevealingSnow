import datetime
import json

import pandas as pd
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


def make_csv_response(data: pd.DataFrame, status=200, headers=None):
    response = Response(
        data.to_csv(index=False),
        status=status,
        headers=headers,
        mimetype='text/csv'
    )

    response.headers['Content-Disposition'] = 'attachment; filename=patients.csv'
    return response
