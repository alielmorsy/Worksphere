from rest_framework.permissions import BasePermission

from management import models
from management.exceptions import NotAllowed
from django.utils.translation import gettext as _


class DefaultPermissions:
    # General Purpose
    CAN_READ = 1 << 1
    CAN_WRITE = 2 << 1 | CAN_READ

    # For Chat System
    CREATE_REMOVE_CHANNELS = 3 << 1
    REACT_ON_CHANNEL = 4 << 1
    DELETE_MESSAGES = 5 << 1

    # Cloud space
    CAN_UPLOAD_FILES = 5 << 1
    CAN_DOWNLOAD_FILES = 6 << 1

    # Admin
    CAN_CHANGE_SETTINGS = 7 << 1

    REGULAR_USER = CAN_READ | CAN_WRITE | REACT_ON_CHANNEL | CAN_UPLOAD_FILES | CAN_DOWNLOAD_FILES

    ADMIN = REGULAR_USER | CAN_CHANGE_SETTINGS | CREATE_REMOVE_CHANNELS


class IsUserCompany(BasePermission):
    """
    Permission class that only required for any request requires checks whether the user part of the company
    or not. If not part of company a new error will be sent.
    """

    def has_permission(self, request, view):
        user = request.user
        company_id = view.get_company_id()
        try:
            models.Company.objects.get(_id=company_id, users__user___id=user.pk)
            return True
        except:
            raise NotAllowed(detail=_("Not Allowed User, Or Invalid Company."))
