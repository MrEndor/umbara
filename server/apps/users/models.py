from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.core import models as core_models
from server.apps.users.logic.queries import user


class UserWithProfile(User):
    """User proxy model."""

    objects = (  # noqa: WPS110
        user.UserWithProfileManager()  # type: ignore[assignment]
    )

    class Meta(User.Meta):
        proxy = True

    def create_profile(self) -> 'Profile':
        """Method for create profile."""
        return Profile.objects.create(
            user=self,
        )


class Profile(core_models.ImageMixin, models.Model):
    """Profile Item Model."""

    user = models.OneToOneField(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('birthday'),
    )
    coffee_count = models.IntegerField(
        default=0,
        verbose_name=_('coffe count'),
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        """Method for string the model."""
        return str(self.user.username)
