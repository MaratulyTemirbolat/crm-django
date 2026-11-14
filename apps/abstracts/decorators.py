# Python modules
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar, Literal

# Django modules
from django.db.models import Model, Manager, QuerySet

# Django REST Framework
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

# Project modules


T = TypeVar("T", bound=Model)

# VALIDATE_OPTIONS = Literal["query_params", "request_data", "both"]

def validate_serializer_data(
    serializer_class: Type[Serializer],
    many: bool = False,
    # what_to_validate: VALIDATE_OPTIONS = "request_data",
) -> Callable:
    """Decorator to preprocess the request data validation."""

    def decorator(
        func: Callable[[DRFRequest, tuple[Any, ...], dict[Any, Any]], DRFResponse],
    ) -> Callable:

        @wraps(func)
        def wrapper(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[Any, Any],
        ):
            """Validate the request data using the provided serializer class."""
            local_context: dict[str, Any] = {"request": request}

            # data: dict[str, Any] = request.data if what_to_validate == "request_data" else request.query_params if what_to_validate == "query_params" else {**request.data, **request.query_params}
            if request.method in ("POST", "PUT", "PATCH"):
                data = request.data
            else:
                data = request.query_params
                # url_path?is_active=true&email=t.maratuly@kbtu.kz
                # query_params = {"is_active": "true", "email": "t.maratuly@kbtu.kz"}

            if "pk" in kwargs:
                local_context["pk"] = int(kwargs["pk"])

            if "object" in kwargs:
                local_context["object"] = kwargs["object"]

            serializer: Serializer = serializer_class(
                instance=local_context.get("object"),
                data=data,
                context=local_context,
                many=many,
                partial=request.method == "PATCH"
            )
            if serializer.is_valid():
                kwargs["validated_data"] = serializer.validated_data.copy()
                kwargs["serializer"] = serializer
                return func(self, request, *args, **kwargs)
            else:
                return DRFResponse(
                    data=serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )

        return wrapper

    return decorator


def find_queryset_object_by_query_pk(
    queryset: QuerySet[T] | Manager[T],
    entity_name: str,
) -> Callable:
    """
    Decorator to find an object by its primary key in the queryset.


    - entity_name: The name of the entity which will be used in the error message.
    """

    def decorator(
        func: Callable[[DRFRequest, tuple[Any, ...], dict[Any, Any]], DRFResponse],
    ) -> Callable:

        @wraps(func)
        def wrapper(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[Any, Any],
        ) -> DRFResponse:
            """Get the object from the queryset and pass it to the view. If the object is not found, return a 404 response."""
            pk: Optional[str] = kwargs.get("pk", None)
            if not pk:
                return DRFResponse(
                    data={
                        "details": [
                            f"{entity_name} ID is required."
                        ]
                    },
                    status=HTTP_400_BAD_REQUEST,
                )

            if not pk.isdigit():
                return DRFResponse(
                    data={
                        "details": [
                            f"{entity_name} ID must be a number."
                        ]
                    },
                    status=HTTP_400_BAD_REQUEST,
                )
            try:
                kwargs["object"] = queryset.get(pk=pk)
                return func(self, request, *args, **kwargs)
            except queryset.model.DoesNotExist:
                return DRFResponse(
                    data={
                        "details": [
                            f"{entity_name} with ID {pk} hasn't been found."
                        ]
                    },
                    status=HTTP_404_NOT_FOUND,
                )
            except queryset.model.MultipleObjectsReturned:
                return DRFResponse(
                    data={
                        "details": [
                            f"Multiple {entity_name} objects returned for ID {pk}."
                        ],
                    },
                    status=HTTP_400_BAD_REQUEST,
                )

        return wrapper

    return decorator