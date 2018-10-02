import logging
import os

from flask_env import MetaFlaskEnv

from snow import constants as C

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
load_environment_file(os.environ.get(C.RSENV_FILE) or C.DEFAULT_ENVIRONMENT_FILE)


class Configuration(metaclass=MetaFlaskEnv):
    DEBUG = True

    LOGGING_CONFIG_FILE = 'logging.yaml'
    SCREENING_DATA_FILE = "screening.csv"
