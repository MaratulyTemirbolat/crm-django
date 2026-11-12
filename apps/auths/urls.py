from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.auths.views import CustomUserViewSet


router = DefaultRouter(trailing_slash=False)

router.register(
    prefix="users",
    viewset=CustomUserViewSet,
    basename="customuser",
)

urlpatterns = [
    path("v1/", include(router.urls)),
]