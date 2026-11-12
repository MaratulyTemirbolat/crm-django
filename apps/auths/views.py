from typing import Any

from django.db.models import QuerySet

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from apps.auths.models import CustomUser
from apps.auths.serializers import (
    CustomUserBaseSerializer,
    CustomUserListSerializer,
    CustomUserCreateSerializer,
    CustomUserDetailSerializer,
)


class CustomUserViewSet(ViewSet):
    """
    Custom User ViewSet for handling user-related actions.
    """

    queryset = CustomUser.objects
    serializer_class = CustomUserBaseSerializer

    def list(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Returns a list of all users.
        """
        users = self.queryset.all()[:5]
        serializer = CustomUserListSerializer(users, many=True)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def create(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Creates a new User instance endpoint.
        """
        serializer = CustomUserCreateSerializer(data=request.data)
        valid: bool = serializer.is_valid()
        if not valid:
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
        new_user: CustomUser = serializer.save()
        new_user.set_password(serializer.validated_data["password"])
        new_user.save()
        return DRFResponse(
            data=CustomUserDetailSerializer(new_user).data,
            status=HTTP_201_CREATED
        )

    def retrieve(self, request: DRFRequest, pk: str, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Retrieves a specific User instance by ID.
        """
        try:
            user: CustomUser = self.queryset.get(id=pk)
        except CustomUser.DoesNotExist:
            return DRFResponse(
                data={"detail": f"User with id {pk} does not exist."},
                status=HTTP_404_NOT_FOUND,
            )
        serializer = CustomUserDetailSerializer(user)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def delete(self, request: DRFRequest, pk: str, *args: Any, **kwargs: Any) -> DRFResponse:
        try:
            user: CustomUser = self.queryset.get(id=pk)
        except CustomUser.DoesNotExist:
            return DRFResponse(
                data={"detail": f"User with id {pk} does not exist."},
                status=HTTP_404_NOT_FOUND,
            )
        user.delete()
        return DRFResponse(
            status=HTTP_204_NO_CONTENT,
        )
