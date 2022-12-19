import functools
from http import HTTPStatus
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
)

from ..utils.handler import SPSError, ErrorType
from ..utils.db import get_db

from flask import (
    request, g,
)
from bson import ObjectId
from flask_restful import Resource


class Register(Resource):

    def post(self):
        """
        Register Endpoint

        Endpoint to register a new user
        ---
        tags:
            - Auth
        parameters:
            - username:
                in: body
                type: string
                required: true
            - password:
                in: body
                type: string
                required: true
        responses:
            201:
                description: User created
            400:
                description: Bad request
            401:
                description: Invalid credentials
        """
        username = request.json['username']
        password = request.json['password']

        db = get_db()

        if not username or not password:
            raise SPSError(*ErrorType.BAD_REQUEST.value)

        if len(list(db.user.find({'username': username}))) > 0:
            raise SPSError(*ErrorType.USERNAME_ALREADY_TAKEN.value)
        else:
            db.user.insert_one({
                'username': username,
                'password': generate_password_hash(password),
            })
            return {'message': 'User created'}, HTTPStatus.CREATED


class Login(Resource):

    def post(self):
        """
        Login Endpoint

        Endpoint to login with username and password
        ---
        tags:
            - Auth
        parameters:
            - username:
                in: body
                type: string
                required: true
            - password:
                in: body
                type: string
                required: true
        responses:
            200:
                description: Login success
                response:
                    token:
                        type: string
            400:
                description: Bad request
            401:
                description: Invalid credentials
        """
        username = request.json['username']
        password = request.json['password']
        db = get_db()

        user = db.user.find_one({'username': username})
        if (user is None) or not check_password_hash(user['password'], password):
            raise SPSError(*ErrorType.INVALID_CREDENTIALS.value)

        access_token = create_access_token(identity=user['_id'].__str__())
        return {'token': access_token}, HTTPStatus.OK


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):

        try:
            verify_jwt_in_request()
        except Exception:
            raise SPSError(*ErrorType.INVALID_CREDENTIALS.value)

        identity = get_jwt_identity()
        db = get_db()
        user = db.user.find_one({'_id': ObjectId(identity)})
        if user is None:
            raise SPSError(*ErrorType.INVALID_CREDENTIALS.value)

        g.user = user
        return view(**kwargs)

    return wrapped_view
