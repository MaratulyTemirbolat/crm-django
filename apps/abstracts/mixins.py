# Python
from typing import (
    Any,
    Optional,
    Type,
)

# DRF
from rest_framework.pagination import BasePagination
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK


class DRFResponseMixin:
    """Mixin to get DRF response."""

    def get_drf_response(
        self,
        request: DRFRequest,
        data: Any,
        serializer_class: Type[Serializer],
        many: bool = False,
        paginator: Optional[BasePagination] = None,
        status_code: int = HTTP_200_OK,
    ) -> DRFResponse:
        serializer_context: dict[str, Any] = {"request": request}
        if paginator and many:
            objects: list = paginator.paginate_queryset(
                queryset=data, request=request, view=self
            )
            serializer: Serializer = serializer_class(
                objects, many=many, context=serializer_context
            )
            return paginator.get_paginated_response(serializer.data)

        serializer: Serializer = serializer_class(
            data, many=many, context=serializer_context
        )
        return DRFResponse(data=serializer.data, status=status_code)