import datetime
import json
import time
import zipfile
from io import BytesIO

import pandas as pd
from flask import Response, send_file


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


# Adapted from: https://stackoverflow.com/a/27337047/228591
def make_zip_response(filename, files):
    mem = BytesIO()
    with zipfile.ZipFile(mem, 'w') as zf:
        for name, content in files.items():
            data = zipfile.ZipInfo(name)
            data.date_time = time.localtime(time.time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, content)

    mem.seek(0)
    return send_file(mem, attachment_filename=filename, as_attachment=True)
