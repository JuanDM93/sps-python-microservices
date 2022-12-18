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
        if not app.config.get('DATABASE'):
            app.config['DATABASE'] = os.environ.get('MONGODB_URI')

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # app setup
    from .utils import db
    db.init_app(app)

    return app
