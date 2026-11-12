from typing import Any

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    EmailField,
    CharField,
    ValidationError,
)

from apps.auths.models import CustomUser


class UserLoginSerializer(Serializer):
    """
    Serializer for user login.
    """

    email = EmailField(
        required=True,
        max_length=CustomUser.EMAIL_MAX_LENGTH,
    )
    password = CharField(
        required=True,
        max_length=CustomUser.PASSWORD_MAX_LENGTH,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "email",
            "password",
        )

    def validate_email(self, value: str) -> str:
        """Validates the email field."""
        return value.lower()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validates the input data."""
        email: str = attrs["email"]
        password: str = attrs["password"]

        user: CustomUser | None = CustomUser.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                detail={
                    "email": [f"User with email '{email}' does not exist."]
                }
            )

        if not user.check_password(raw_password=password):
            raise ValidationError(
                detail={
                    "password": ["Incorrect password."]
                }
            )

        attrs["user"] = user    

        return super().validate(attrs)


class CustomUserBaseSerializer(ModelSerializer):
    """Base serializer for CustomUser model."""

    class Meta:
        """
        Meta data of the Serializer.
        """

        model = CustomUser
        fields = "__all__"


class CustomUserListSerializer(CustomUserBaseSerializer):
    """Serializer for listing CustomUser instances."""

    class Meta(CustomUserBaseSerializer.Meta):
        """
        Meta data of the Serializer.
        """

        fields = (
            "id",
            "email",
            "full_name",
        )

class CustomUserDetailSerializer(CustomUserBaseSerializer):
    """Serializer for displaying detail CustomUser instances."""

    class Meta(CustomUserBaseSerializer.Meta):
        """
        Meta data of the Serializer.
        """

        fields = (
            "id",
            "email",
            "full_name",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class CustomUserCreateSerializer(CustomUserBaseSerializer):
    """Serializer for creating CustomUser instances."""

    class Meta(CustomUserBaseSerializer.Meta):
        """
        Meta data of the Serializer.
        """

        fields = (
            "email",
            "full_name",
            "password",
        )


class CustomUserUpdateSerializer(CustomUserBaseSerializer):
    """Serializer for updating CustomUser instances."""

    class Meta(CustomUserBaseSerializer.Meta):
        """
        Meta data of the Serializer.
        """

        fields = (
            "email",
            "full_name",
        )
