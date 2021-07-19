from rest_framework import status
from rest_framework.exceptions import APIException


class FunballerNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "not found"
    default_code = "not_found"


class FixtureNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "not found"
    default_code = "not_found"


class GamedayNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "not found"
    default_code = "not_found"


class GameweekNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "not found"
    default_code = "not_found"


class ChoicesNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "not found"
    default_code = "not_found"


class TeamNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "not found"
    default_code = "not_found"


class GameweekDeadlinePassedError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "bad request"
    default_code = "bad_request"
