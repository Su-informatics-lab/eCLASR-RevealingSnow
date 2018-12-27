import logging.config
import os

import yaml
from flask import Flask, request

from snow import constants as C


# Adapted From: https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
def _setup_logging(configfile, default_level=logging.INFO):
    if os.path.exists(configfile):
        with open(configfile, 'rt') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def log_request_info():
    import logging
    logger = logging.getLogger(__name__)

    logger.debug(
        "%s - %s - %s",
        request.remote_addr,
        request.method,
        request.url
    )


def create_app(configuration=None):
    from snow import config
    from snow import query
    from snow import model
    from snow import export
    from snow import features

    from snow.tracking import tracking
    from snow.ptscreen import pscr

    app = Flask(__name__)
    app.config.from_object(configuration or config.Configuration)

    _setup_logging(app.config[C.LOGGING_CONFIG_FILE])
    app.before_request(log_request_info)

    pscr.init_app(app)
    model.cdm.init_app(app)
    tracking.init_app(app)

    app.add_url_rule('/', view_func=lambda: app.send_static_file('index.html'))
    app.add_url_rule('/stats', 'stats', query.patient_stats)
    app.add_url_rule('/download', 'download', export.download_patients)
    app.add_url_rule('/export', 'export', export.export_patients, methods=['POST'])
    app.add_url_rule('/ymca_stats', 'ymca_stats', query.ymca_stats)
    app.add_url_rule('/model', 'model', model.get_criteria_data_model)
    app.add_url_rule('/features', 'features', features.get_feature_flags)

    return app


def main():
    create_app().run('0.0.0.0', 5000)


def runtornado():
    from snow import wsgi, util
    from tornado import wsgi as twsgi
    from tornado import httpserver
    from tornado import ioloop
    from tornado import netutil

    container = twsgi.WSGIContainer(wsgi.app)
    sockets = netutil.bind_sockets(0, '')

    http_server = httpserver.HTTPServer(container)
    http_server.add_sockets(sockets)

    util.open_browser(sockets)
    ioloop.IOLoop.current().start()
