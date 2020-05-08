import os
from enum import Enum

QUESTIONS_PER_PAGE = 10


class StatusCode(Enum):
    """Enum to maintain status codes."""

    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_405_METHOD_NOT_ALLOWED = 405
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_500_INTERNAL_SERVER_ERROR = 500


class ErrorMessage(Enum):
    MISSING_AUTHORIZATION = 'Authorization header in request headers is mandatory.'
    MISSING_BEARER = 'Authorization header must start with "Bearer".'
    MISSING_TOKEN = 'Authorization header must have token.'
    MISSING_BEARER_TOKEN = 'Authorization header must be a Bearer token.'
    AUTHORIZATION_MALFORMED = 'Authorization malformed.'
    TOKEN_EXPIRED = 'Token Expired.'
    INVALID_CLAIMS = 'Ivalid claims. Please, check the audience and issuer.'
    UNABLE_TO_PARSE = 'Unable to parse authentication token.'
    INVALID_KEY = 'Unable to find the appropriate key.'


DATABASE_CONFIGURATION = {
    'username': os.environ.get('DATABASE_USER') or '',
    'password': os.environ.get('DATABASE_PASSWORD') or '',
    'name': os.environ.get('DATABASE_NAME') or 'trivia',
    'host': os.environ.get('DATABASE_HOST') or 'localhost',
    'port': os.environ.get('DATABASE_PORT') or '5432',
}

DATABASE_PATH = "postgres://{username}:{password}@{host}:{port}/{name}".format(
    **DATABASE_CONFIGURATION
)

DATABASE_URL = 'postgres://wsutscdutixvob:657152b3032643d1b3f72467a8dd0f5c658ec5c91786e0446704fb59879c7a2b@ec2-50-17-21-170.compute-1.amazonaws.com:5432/d5bnhi6a2qsut6'
