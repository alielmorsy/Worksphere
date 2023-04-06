from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException

from rest_framework import status


class NotAllowed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Not Allowed Request.")
    default_code = "Not-Allowed-Management-Request"
