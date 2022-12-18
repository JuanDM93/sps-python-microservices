from http import HTTPStatus
from flask_restful import MethodView

from ..utils.db import get_db


class Health(MethodView):
    """Health check API"""

    def get(self):
        """
        Health check Endpoint
        ---
        tags:
            - Health
        responses:
            200:
                description: Health check

        """
        get_db().command('ping')
        return {'status': 'ok'}, HTTPStatus.OK
