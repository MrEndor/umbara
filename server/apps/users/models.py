import typing

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.core import models as core_models

if typing.TYPE_CHECKING:
    User: typing.TypeAlias = AbstractUser
else:
    User = get_user_model()


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
