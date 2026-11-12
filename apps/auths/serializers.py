from rest_framework.serializers import ModelSerializer

from apps.auths.models import CustomUser


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
