from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import (
    CharField,
    BooleanField,
    ForeignKey,
    DecimalField,
    UniqueConstraint,
    TextField,
    ManyToManyField,
    PROTECT,
)

from apps.abstracts.models import AbstractBaseModel


class Project(AbstractBaseModel):
    """Projects database table."""

    NAME_MAX_LEN = 70

    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    members = ManyToManyField(
        to=User,
        blank=True,
        through="UserProject",
        through_fields=("project", "user"),
        related_name="joined_projects"
    )


class UserProject(AbstractBaseModel):
    """Relationship table between User and Project tables under a specified role."""

    user = ForeignKey(
        to=User,
        on_delete=PROTECT,
    )
    project = ForeignKey(
        to=Project,
        on_delete=PROTECT
    )
    role = ForeignKey(
        to="Role",
        on_delete=PROTECT
    )

    class Meta:
        """Meta data for the table."""

        constraints = [
            UniqueConstraint(
                fields=("user", "project"),
                name="unique_user_project",
            )
        ]



class Role(AbstractBaseModel):
    """Role database table."""

    NAME_MAX_LEN = 50

    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    readonly_permission = BooleanField(
        default=False
    )
    create_permission = BooleanField(
        default=False
    )
    update_permission = BooleanField(
        default=False
    )
    delete_permission = BooleanField(
        default=False
    )


class Status(AbstractBaseModel):
    """Statuses database table."""

    NAME_MAX_LEN = 50
    ORDER_MAX_DIGITS = 10
    ORDER_DECIMAL_PLACES = 3
    ORDER_DEFAULT_VALUE = Decimal("0.0")

    name = CharField(
        max_length=NAME_MAX_LEN
    )
    project = ForeignKey(
        to=Role,
        on_delete=PROTECT,
    )
    order = DecimalField(
        max_digits=ORDER_MAX_DIGITS,
        decimal_places=ORDER_DECIMAL_PLACES,
        default=ORDER_DEFAULT_VALUE,
    )

    class Meta:
        """Meta data of the table."""

        constraints = [
            UniqueConstraint(
                fields=("name", "project",),
                name="unique_project_status",
            ),
        ]


class Task(AbstractBaseModel):
    """Task database table."""

    TITLE_MAX_LEN = 200

    title = CharField(
        max_length=TITLE_MAX_LEN
    )
    project = ForeignKey(
        to=Project,
        on_delete=PROTECT,
    )
    description = TextField(
        blank=True,
        default="",
    )
    author = ForeignKey(
        to=User,
        on_delete=PROTECT,
        related_name="created_tasks"
    )
    assignees = ManyToManyField(
        to=User,
        blank=True,
        related_name="assigned_tasks"
    )
