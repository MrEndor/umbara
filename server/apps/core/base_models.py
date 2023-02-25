from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from server.apps.core import constants
from server.apps.core.normalize import normalize


class BaseModel(models.Model):
    """Base model."""

    name = models.CharField(
        max_length=constants.MAX_NAME_LENGTH,
        verbose_name=_('name'),
        help_text=format_lazy(
            _('Maximum length {maximum}'),
            maximum=constants.MAX_NAME_LENGTH,
        ),
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_('published'),
    )

    class Meta:
        verbose_name = 'BaseModel'
        abstract = True


class Slugable(models.Model):
    """Abstract model for object slug."""

    slug = models.SlugField(
        max_length=constants.MAX_SLUG_LENGTH,
        unique=True,
        validators=[
            validators.RegexValidator(constants.REGEX_SLUG),
        ],
    )

    class Meta:
        verbose_name = 'Slugable'
        abstract = True


class NormalizedName(BaseModel):
    """Abstract model for normalized name."""

    normalized_name = models.CharField(  # noqa: DJ01
        max_length=constants.MAX_NAME_LENGTH,
        editable=False,
        unique=True,
        null=True,
        verbose_name=_('normalized name'),
    )

    class Meta:
        verbose_name = 'Normalized name'
        abstract = True

    def clean(self) -> None:
        """Validate model."""
        if self.normalized_name:
            return

        name = normalize(self.name)

        if self.__class__.objects.filter(normalized_name=name).exists():
            raise ValidationError({'name': _('Name is already exists')})

    def save(
        self, *args, **kwargs,
    ) -> None:
        """Save model."""
        self.normalized_name = normalize(self.name)
        super().save(*args, **kwargs)
