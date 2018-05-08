import logging.config
import os

import yaml
from flask import Flask

from snow import constants as  C


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
    from snow import query
    from snow import model
    from snow.ptscreen import pscr

    app = Flask(__name__)
    app.config.from_object(config.Configuration)
    _setup_logging(app.config[C.LOGGING_CONFIG_FILE])

    pscr.init_app(app)
    model.cdm.init_app(app)

    app.add_url_rule('/stats', 'stats', query.patient_stats)
    app.add_url_rule('/model', 'model', model.get_criteria_data_model)

    return app
