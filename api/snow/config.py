import logging
import os

from flask_env import MetaFlaskEnv

from snow import constants as C
from snow import util

logger = logging.getLogger(__name__)


def load_environment_file(filename):
    # Load the contents of the file (key=value) to the environment
    if os.path.exists(filename):
        logger.debug("Importing environment from %s", filename)

        for line in open(filename):
            line = line.strip()
            if not line.startswith('#'):
                key, value = line.split('=')
                os.environ[key] = value


# Load any external environment variables before the configuration class definition
load_environment_file(
    os.environ.get(C.RSENV_FILE) or util.file_in_package(C.DEFAULT_ENVIRONMENT_FILE)
)


class Configuration(metaclass=MetaFlaskEnv):
    DEBUG = True

    LOGGING_CONFIG_FILE = util.file_in_package('logging.yaml')
    SCREENING_DATA_FILE = util.file_in_package("screening.csv")

    TRACKING_API_ENABLED = False
    TRACKING_API_URL_BASE = None
    TRACKING_API_EXPORT_PATH = None
    TRACKING_API_AUTH_USER = None
    TRACKING_API_AUTH_PASS = None
    TRACKING_API_TIMEOUT = 5
