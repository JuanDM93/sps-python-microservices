import enum
from flask import current_app
from http import HTTPStatus
from werkzeug.exceptions import HTTPException


class SPSError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"message": self.message, "status_code": self.status_code}

    def to_response(self):
        return self.to_dict(), self.status_code


def error_handler(e):
    """Global error handler"""
    if isinstance(e, HTTPException):
        return {'message': e.description}, e.code

    if isinstance(e, SPSError):
        return e.to_response()

    if current_app.debug:
        current_app.log_exception(e)
        return e, HTTPStatus.INTERNAL_SERVER_ERROR
    return {'message': "Internal Server Error"}, HTTPStatus.INTERNAL_SERVER_ERROR


class ErrorType(enum.Enum):

    UNKNOWN_ERROR = ("Unknown error", HTTPStatus.INTERNAL_SERVER_ERROR)

    BAD_REQUEST = ("Bad request", HTTPStatus.BAD_REQUEST)

    AUTH_REQUIRED = ("Authorization required", HTTPStatus.BAD_REQUEST)

    INVALID_CREDENTIALS = ("Invalid credentials", HTTPStatus.UNAUTHORIZED)

    USERNAME_ALREADY_TAKEN = ("Username already taken", HTTPStatus.BAD_REQUEST)

    TITLE_REQUIRED = ("Title is required", HTTPStatus.BAD_REQUEST)

    BLOG_NOT_FOUND = ("Blog not found", HTTPStatus.NOT_FOUND)
