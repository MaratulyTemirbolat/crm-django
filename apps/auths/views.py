from typing import Any
from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import QuerySet

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
)

from apps.auths.models import CustomUser
from apps.abstracts.mixins import DRFResponseMixin
from apps.abstracts.decorators import validate_serializer_data, find_queryset_object_by_query_pk
from apps.auths.serializers import (
    CustomUserBaseSerializer,
    CustomUserListSerializer,
    CustomUserCreateSerializer,
    CustomUserDetailSerializer,
    CustomUserUpdateSerializer,
    UserLoginSerializer,
)
from apps.crm.serializers.tasks import TaskListSerializer


class CustomUserViewSet(DRFResponseMixin, ViewSet):
    """
    Custom User ViewSet for handling user-related actions.
    """

    queryset = CustomUser.objects
    serializer_class = CustomUserBaseSerializer

    @action(
        methods=("POST",),
        detail=False,
        url_path="login",
        url_name="login",
    )
    @validate_serializer_data(serializer_class=UserLoginSerializer)
    def login(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle user login.
        Parameters:
            request: DRFRequest
                The request object.
            *args: tuple
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.

        Returns:
            DRFResponse
                Response containing user data or error message.
        """

        serializer: UserLoginSerializer = kwargs["serializer"]

        user: CustomUser = serializer.validated_data.pop("user")

        # Generate JWT tokens
        refresh_token: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh_token.access_token)

        return DRFResponse(
            data={
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "access": access_token,
                "refresh": str(refresh_token),
            },
            status=HTTP_200_OK
        )


    def list(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Returns a list of all users.
        """
        users = self.queryset.all()[:5]
        return self.get_drf_response(
            request=request,
            data=users,
            serializer_class=CustomUserListSerializer,
            many=True,
        )

    @validate_serializer_data(serializer_class=CustomUserCreateSerializer)
    def create(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Creates a new User instance endpoint.
        """
        serializer: CustomUserCreateSerializer = kwargs["serializer"]
        new_user: CustomUser = serializer.save()
        new_user.set_password(serializer.validated_data["password"])
        new_user.save()
        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    @find_queryset_object_by_query_pk(queryset=queryset, entity_name="User")
    def retrieve(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Retrieves a specific User instance by ID.
        """
        user: CustomUser = kwargs["object"]
        return self.get_drf_response(
            request=request,
            data=user,
            serializer_class=CustomUserDetailSerializer,
        )

    # TODO: It is not called
    @find_queryset_object_by_query_pk(queryset=queryset, entity_name="User")
    def delete(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Deletes a specific User instance by ID.
        """
        user: CustomUser = kwargs["object"]
        user.delete()
        return DRFResponse(status=HTTP_204_NO_CONTENT)

    @find_queryset_object_by_query_pk(queryset=queryset, entity_name="User")
    @validate_serializer_data(serializer_class=CustomUserUpdateSerializer)
    def update(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Updates a specific User instance by ID.
        """
        serializer: CustomUserUpdateSerializer = kwargs["serializer"]
        updated_user: CustomUser = serializer.save()
        return self.get_drf_response(
            request=request,
            data=updated_user,
            serializer_class=CustomUserDetailSerializer,
        )

    @find_queryset_object_by_query_pk(queryset=queryset, entity_name="User")
    @validate_serializer_data(serializer_class=CustomUserUpdateSerializer)
    def partial_update(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Partially updates a specific User instance by ID.
        """

        serializer: CustomUserUpdateSerializer = kwargs["serializer"]
        serializer.save()
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    @action(
        methods=("GET",),
        detail=True,
        url_path="tasks",
        url_name="tasks",
    )
    @find_queryset_object_by_query_pk(queryset=queryset, entity_name="User")
    def get_user_tasks(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Retrieves tasks associated with a specific User instance by ID.
        """
        user: CustomUser = kwargs["object"]
        return self.get_drf_response(
            request=request,
            data=user.created_tasks.all(),  # Task.objects.filter(author_id=user.id)
            serializer_class=TaskListSerializer,
            many=True,
        )
        