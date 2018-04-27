from flask_env import MetaFlaskEnv


class Configuration(metaclass=MetaFlaskEnv):
    DEBUG = True

    LOGGING_CONFIG_FILE = 'logging.yaml'
    SCREENING_DATA_FILE = "screening.csv"
