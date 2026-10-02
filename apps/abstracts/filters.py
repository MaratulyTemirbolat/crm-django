from django.contrib.admin import SimpleListFilter


class IsDeletedListFilter(SimpleListFilter):
    title = "Is deleted object"
    parameter_name = "is_deleted"

    DELETED_KEY = "deleted"
    NONDELETED_KEY = "non-deleted"

    def lookups(self, request, model_admin) -> list[tuple[str, str]]:
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            (self.DELETED_KEY, "Deleted"),
            (self.NONDELETED_KEY, "Not deleted"),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == self.DELETED_KEY:
            return queryset.filter(deleted_at__isnull=False) # WHERE deleted_at IS NOT NULL
        if self.value() == self.NONDELETED_KEY:
            return queryset.filter(deleted_at__isnull=True)  # WHERE deleted_at IS NULL
        return queryset.all() # SELECT * FROM custom_users;