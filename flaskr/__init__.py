import os
from flask import Flask, Blueprint
from flask_restful import Api


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
    from .utils import db, handler
    db.init_app(app)
    app.register_error_handler(Exception, handler.error_handler)

    # index
    from .utils.index import index_bp
    app.register_blueprint(index_bp)

    # api
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api = Api(api_bp)

    # health
    from .apis.health import Health
    api.add_resource(Health, '/health')

    # auth
    from .apis.auth import Register, Login
    api.add_resource(Register, '/auth/register')
    api.add_resource(Login, '/auth/login')

    # blogs
    from .apis.blogs import BlogList, BlogDetail
    api.add_resource(BlogList, '/blogs')
    api.add_resource(BlogDetail, '/blogs/<string:id>')

    # blueprints
    from .apis.docs import swagger_bp
    app.register_blueprint(swagger_bp)
    app.register_blueprint(api_bp)

    return app
