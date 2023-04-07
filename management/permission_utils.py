from rest_framework.permissions import BasePermission

from management import models
from management.exceptions import NotAllowed
from django.utils.translation import gettext as _


class DefaultPermissions:
    # General Purpose
    CAN_READ = 1 << 1
    CAN_WRITE = 2 << 1 | CAN_READ

    # For Chat System
    CREATE_REMOVE_CHANNELS = 4 << 1
    REACT_ON_CHANNEL = 8 << 1
    DELETE_MESSAGES = 16 << 1

    # Cloud space
    CAN_UPLOAD_FILES = 32 << 1
    CAN_DOWNLOAD_FILES = 64 << 1

    # Admin
    CAN_CHANGE_SETTINGS = 128 << 1

    CAN_ADD_TASKS = 256 << 1

    REGULAR_USER = CAN_WRITE | REACT_ON_CHANNEL | CAN_UPLOAD_FILES | CAN_DOWNLOAD_FILES | CAN_ADD_TASKS

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
            return models.Company.objects.get(_id=company_id, users__user___id=user.pk)
        except:
            raise NotAllowed(detail=_("Not Allowed User, Or Invalid Company."))


"""
- Setup websocket for messages. (Ali)
- Setup Task API.
"""


class DoesUserHavePermission(IsUserCompany):
    def has_permission(self, request, view):
        company = super().has_permission(request, view)
        company_user = company.users.get(user___id=request.user.pk)
        roles = company_user.roles

        for role in roles:
            permissions = role.permissions
            if permissions & view.default_permissions == view.default_permissions:
                return True
        raise RuntimeWarning("Bad Request.")  # TODO: Need to look pretty.
