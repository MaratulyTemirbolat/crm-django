from django.contrib.admin import register, ModelAdmin
from django.utils.safestring import mark_safe
from django.core.handlers.wsgi import WSGIRequest

from apps.auths.models import CustomUser
from apps.abstracts.filters import IsDeletedListFilter


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """CustomUser model admin configuration class."""


    list_display = (
        "id",
        "email",
        "full_name",
        "is_active",
        "is_deleted",
    )
    list_filter = (
        "is_staff",
        "is_active",
        IsDeletedListFilter,
    )
    # fields = (
    #     "id",
    #     "email",
    # )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    search_fields = (
        "id",
        "email",
    )
    filter_horizontal = (
        "user_permissions",
    )
    # list_editable = (
    #     "full_name",
    # )
    fieldsets = (
        (
            'General information',
            {
                'fields': (
                    "id",
                    "email",
                    "full_name",
                )
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    ("is_staff", "is_active"),
                    "user_permissions",
                )
            },
        ),
        (
            'Date and time information',
            {
                'fields': (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            },
        ),
    )
    list_per_page = 50
    list_display_links = (
        "id",
        "email",
    )
    save_on_top = True


    def has_module_permission(self, request: WSGIRequest) -> bool:
        """
        Returns True to make a model visible, otherwise hides it from admin panel
        """
        return True

    def has_add_permission(self, request: WSGIRequest) -> bool:
        """
        Returns False to make a creation form unreachable and forbids with permission.
        """
        return True

    def has_change_permission(self, request: WSGIRequest, obj: CustomUser | None = None) -> bool:
        """
        Returns False to make an object which we observe non-editable for the current User.
        """
        return False

    def has_view_permission(self, request: WSGIRequest, obj: CustomUser | None = None) -> bool:
        return True

    def has_delete_permission(self, request: WSGIRequest, obj: CustomUser | None = None) -> bool:

        cur_user: CustomUser | None = getattr(request, "user", None)
        if obj and cur_user and cur_user == obj:
            return False

        if obj and obj.deleted_at is None:
            return True
        return False


    def get_readonly_fields(self, request: WSGIRequest, obj: CustomUser | None = None) -> tuple[str, ...]:
        if obj:
            return (
                "email",
                "password",
            ) + self.readonly_fields
        return self.readonly_fields


    def is_deleted(self, instance: CustomUser | None = None) -> str:
        """Return html wrapped information about user existence."""

        if isinstance(instance, CustomUser):
            if not instance.deleted_at:
                return mark_safe('<span style="color: green; font-weight: bold;">Not deleted</span>')
            else:
                return mark_safe('<span style="color: red; font-weight: bold;">Deleted</span>')
    
        return mark_safe('<span style="color: gray; font-weight: bold;">Unknown</span>')
    is_deleted.short_description = "Status"

    # def get_fields(self, request: WSGIRequest, obj: CustomUser | None = None) -> tuple[str, ...]:
    #     current_user: CustomUser | None = request.user
    #     if isinstance(current_user, CustomUser) and "t.maratuly" in current_user.email:
    #         return (
    #             "id",
    #         )
    #     return (
    #         "id",
    #         "email",
    #         ("full_name", "password",),
    #     )


class A:

    def __init__(self, value: str):
        self.id = value

    def __eq__(self, obj: "A") -> bool:
        if self.id == obj.id:
            return True
        return False


a = A("A")
b = A("A")


print(a == b)