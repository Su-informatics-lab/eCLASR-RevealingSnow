#!/usr/bin/env python
import io
import os
import re

from setuptools import setup

with io.open('./snow/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name='snow',
    version=version,
    description='US POINTER Visualization Tool',
    long_description=long_description,
    author='Ryan Barnard',
    author_email='rybarnar@wakehealth.edu',
    license='GPL',
    packages=['snow'],
    package_data={
        'snow': ['data/*.yml', 'logging.yaml', '.config.env'] + package_files('snow/static')
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'Start Visualization = snow.app:runtornado',
        ],
    },
    install_requires=[
        'Flask',
        'Flask-Env',
        'pandas',
        'PyYAML',
        'requests',
        'responses',
        'tornado'
    ],
    options={
        'app': {
            'formal_name': 'Revealing Snow',
            'bundle': 'edu.wakehealth'
        },

        # Desktop/laptop deployments
        'macos': {
            'app_requires': []
        },
        'linux': {
            'app_requires': [
            ]
        },
        'windows': {
            'app_requires': [
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [
            ]
        },
        'android': {
            'app_requires': [
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [
            ]
        },
    }
)
