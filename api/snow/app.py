from flask import Flask


def index():
    return 'Hello, world!'


def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', 'index', index)

    return app