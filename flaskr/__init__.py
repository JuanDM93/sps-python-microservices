import os
from flask import Flask


def create_app(test_config=None):
    """
    Create and configure an instance of the Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile(f'config.py', silent=True)

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    return app
