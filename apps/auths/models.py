from typing import Any

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
)

from apps.abstracts.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    """Custom User Manager to make database requests."""

    def __obtain_user_instance(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Get user instance."""
        if not email:
            raise ValidationError(
                message="Email field is required", code="email_empty"
            )
        if not full_name:
            raise ValidationError(
                message="Full name name is required.", code="full_name_empty"
            )

        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
            **kwargs,
        )
        return new_user

    def create_user(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create Custom user. TODO where is this used?"""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=email,
            full_name=full_name,
            password=password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
        self,
        email: str,
        full_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create super user. Used by manage.py createsuperuser."""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    Custom user model extending AbstractBaseModel.
    """

    EMAIL_MAX_LENGTH = 150
    FULL_NAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 254

    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        db_index=True,
    )
    full_name = CharField(
        max_length=FULL_NAME_MAX_LENGTH,
    )
    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
    )
    # True iff the user is part of the corporoom team, allowing them to access the admin panel
    is_staff = BooleanField(
        default=False,
    )
    # True iff the user can make requests to the backend (include in company)
    is_active = BooleanField(
        default=True,
    )

    REQUIRED_FIELDS = ["full_name"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

