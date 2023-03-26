from typing import Optional

from django.contrib.auth import backends
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Q  # noqa: WPS347
from django.http import HttpRequest

from server.apps.users.models import UserWithProfile


class UserAuthBackend(backends.ModelBackend):
    """Backend authentication with email."""

    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs,
    ) -> Optional[AbstractBaseUser]:
        """Method for auth."""
        if username is None:
            username = kwargs.get(UserWithProfile.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            user = UserWithProfile.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username),
            )
        except UserWithProfile.DoesNotExist:
            UserWithProfile().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
