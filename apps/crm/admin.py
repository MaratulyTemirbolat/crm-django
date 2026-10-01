from django.contrib.admin import ModelAdmin, register

from apps.crm.models import (
    Project,
    UserProject,
    Role,
    Status,
    Task,
)


@register(Project)
class ProjectAdmin(ModelAdmin):
    """
    Project admin class configuration.
    """

    ...


@register(UserProject)
class UserProjectAdmin(ModelAdmin):
    """
    User Project relationship admin class configuration.
    """

    ...


@register(Role)
class RoleAdmin(ModelAdmin):
    """
    Role admin class configuration.
    """

    ...


@register(Status)
class StatusAdmin(ModelAdmin):
    """
    Status admin class configuration.
    """

    ...


@register(Task)
class TaskAdmin(ModelAdmin):
    """
    Status admin class configuration.
    """

    ...
