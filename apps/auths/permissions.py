from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRFRequest

from apps.auths.models import CustomUser


class IsUserOwner(BasePermission):
    """
    Allow access only for users which refer to themselves.
    """

    message = "Permission denied! You don't own this account."

    def has_object_permission(self, request: DRFRequest, view: Any, obj: CustomUser) -> bool:
        """Returns True if the user is me."""
        user: CustomUser = request.user
        return bool(
            user and 
            user.is_authenticated and
            obj.id == user.id
        )


class IsUserOwnerOrAdmin(BasePermission):
    """
    Allow access only for users which refer to themselves.
    """

    message = "Permission denied! You don't own this account."

    def has_object_permission(self, request: DRFRequest, view: Any, obj: CustomUser) -> bool:
        """Returns True if the user is me."""
        user: CustomUser = request.user
        return bool(
            user and 
            user.is_authenticated and
            obj.id == user.id or
            user.is_staff
        )