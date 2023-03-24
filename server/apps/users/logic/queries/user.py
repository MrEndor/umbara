from typing import TYPE_CHECKING, Optional

from django.contrib.auth.models import UserManager
from django.db.models import Prefetch, QuerySet

from server.apps.core import fields
from server.apps.users import models
from server.apps.users.logic.normalization import normalize_email

if TYPE_CHECKING:
    from server.apps.users.models import UserWithProfile  # pragma: no cover


class UserWithProfileManager(UserManager['UserWithProfile']):
    """Query Manager for CatalogItem."""

    def create_user(
        self,
        username: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields,
    ) -> 'UserWithProfile':
        """Method for create user with profile."""
        user = super().create(  # noqa: WPS613
            username=username, email=email, password=password, **extra_fields,
        )
        models.Profile.objects.create(user=user)

        return user

    @classmethod
    def normalize_email(cls, email: Optional[str]) -> str:
        """Method for normalize email by domain."""
        email = super().normalize_email(email)

        return normalize_email(email)

    def list_active_users(self) -> QuerySet['UserWithProfile']:
        """List activate users with profile."""
        profile_prefetch = Prefetch(
            'profile',
            queryset=models.Profile.objects.only(
                fields.get_field_name(models.Profile.image),
                fields.get_field_name(models.Profile.user),
            ),
        )

        return self.filter(
            is_active=True,
        ).prefetch_related(
            profile_prefetch,
        ).only(
            fields.get_field_name(self.model.username),
        )

    def get_user_detail(
        self,
        username: str,
    ) -> Optional['UserWithProfile']:
        """Get user by username with profile."""
        if not self.filter(username=username, is_active=True).exists():
            return None

        profile_prefetch = Prefetch(
            'profile',
            queryset=models.Profile.objects.only(
                fields.get_field_name(models.Profile.image),
                fields.get_field_name(models.Profile.coffee_count),
                fields.get_field_name(models.Profile.birthday),
                fields.get_field_name(models.Profile.user),
            ),
        )

        return self.filter(
            is_active=True,
        ).prefetch_related(
            profile_prefetch,
        ).only(
            fields.get_field_name(self.model.username),
            fields.get_field_name(self.model.email),
            fields.get_field_name(self.model.first_name),
            fields.get_field_name(self.model.last_name),
        ).get(
            username=username,
        )
