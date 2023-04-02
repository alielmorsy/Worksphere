from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException

class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = _('Wrong username or password.')
    default_code = 'invalid-credentials'


class UserDoesnotExist(APIException):
    status_code = 401
    default_detail = _('User Does not exist')
    default_code = 'invalid-credentials'

class ChannelDoesnotExist(APIException):
    status_code = 401
    default_detail = _('Channel Does not exist')
    default_code = 'invalid-credentials'