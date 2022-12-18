from flask import Blueprint, jsonify, current_app as app
from flask_swagger import swagger

swagger_bp = Blueprint('swagger', __name__)


@swagger_bp.route('/spec')
def spec():
    swag = swagger(app)
    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'Flaskr API (SPS)'
    return jsonify(swag)
