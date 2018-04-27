import logging.config
import os

import yaml
from flask import Flask


def index():
    return 'Hello, world!'


# Adapted From: https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
def _setup_logging(configfile, default_level=logging.INFO):
    if os.path.exists(configfile):
        with open(configfile, 'rt') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def create_app():
    from snow import config
    from snow.ptscreen import pscr

    app = Flask(__name__)
    app.config.from_object(config.Configuration)
    _setup_logging(app.config['LOGGING_CONFIG_FILE'])

    pscr.init_app(app)

    app.add_url_rule('/', 'index', index)

    return app
