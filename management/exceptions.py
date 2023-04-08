from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException

from rest_framework import status


class NotAllowed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Not Allowed Request.")
    default_code = "Not-Allowed-Management-Request"

class UserNotExists(APIException):
    status_code = 401
    default_detail = _('User Does not exist')
    default_code = 'invalid-credentials'

class TaskNotExists(APIException):
    status_code = 401
    default_detail = _('Assigned Task  Does not exist')
    default_code = 'invalid-credentials'