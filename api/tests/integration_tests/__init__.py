import inspect
import os
import shutil
import tempfile
from os import path
from unittest import TestCase

from flask_env import MetaFlaskEnv

from snow.app import create_app
from snow.config import Configuration


# Override the environment variable loading metaclass for tests
class NoEnvMeta(MetaFlaskEnv):
    def __init__(self, *args, **kwargs):
        # Bypass MetaFlaskEnv's constructor and call its superclass' constructor
        super(MetaFlaskEnv, self).__init__(*args, **kwargs)


class TestConfig(Configuration, metaclass=NoEnvMeta):
    TRACKING_API_ENABLED = False
    TRACKING_API_URL_BASE = None
    TRACKING_API_EXPORT_PATH = None
    TRACKING_API_AUTH_USER = None
    TRACKING_API_AUTH_PASS = None
    TRACKING_API_TIMEOUT = 5


class TestBase(TestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        self.tempfiles = []
        self.tmpdir = None

    def tearDown(self):
        for handle, filename in self.tempfiles:
            os.close(handle)
            os.unlink(filename)

        if self.tmpdir is not None:
            shutil.rmtree(self.tmpdir)

    def create_app(self, config=None):
        if config is None:
            config = TestConfig

        return create_app(config)

    def get_data_folder(self):
        test_file = inspect.getfile(self.__class__)
        test_dir = path.dirname(path.abspath(test_file))

        return path.join(test_dir, 'data')

    def get_data_file(self, filename):
        test_dir = self.get_data_folder()
        return path.join(test_dir, filename)

    def get_tempfile(self, suffix=None):
        suffix = suffix or '.dat'
        (handle, filename) = tempfile.mkstemp(suffix)

        self.tempfiles.append((handle, filename))
        return filename

    def get_tempdir(self):
        if self.tmpdir is None:
            self.tmpdir = tempfile.mkdtemp()

        return self.tmpdir
