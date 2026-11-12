from rest_framework.serializers import ModelSerializer

from apps.crm.models import Task


class TaskBaseSerializer(ModelSerializer):
    """Base serializer for Task model."""

    class Meta:
        """
        Meta data of the Serializer.
        """

        model = Task
        fields = "__all__"


class TaskListSerializer(TaskBaseSerializer):
    """Serializer for listing Task instances."""

    class Meta(TaskBaseSerializer.Meta):
        """
        Meta data of the Serializer.
        """

        fields = (
            "id",
            "title",
            "project",
            "description",
            "author",
            "assignees",
        )