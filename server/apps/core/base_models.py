from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from server.apps.core import constances
from server.apps.core.normalize import normalize


class Identifiable(models.Model):
    """Abstract model for object identification."""

    id = models.AutoField(
        primary_key=True,
        unique=True,
        editable=False,
        validators=[
            validators.MinValueValidator(constances.MIN_ID),
        ],
        verbose_name='Id',
    )

    class Meta:
        verbose_name = 'Identifiable'
        abstract = True


class Nameable(models.Model):
    """Abstract model for object naming."""

    name = models.CharField(
        max_length=constances.MAX_NAME_LENGTH,
        verbose_name=_('Name'),
        help_text=format_lazy(
            _('Maximum length {maximum}'),
            maximum=constances.MAX_NAME_LENGTH,
        ),
    )

    class Meta:
        verbose_name = 'Nameable'
        abstract = True


class Publishable(models.Model):
    """Abstract model for publishing status."""

    is_published = models.BooleanField(
        default=True,
        verbose_name=_('Published'),
    )

    class Meta:
        verbose_name = 'Publishable'
        abstract = True


class Slugable(models.Model):
    """Abstract model for object slug."""

    slug = models.SlugField(
        max_length=constances.MAX_SLUG_LENGTH,
        unique=True,
        validators=[
            validators.RegexValidator(constances.REGEX_SLUG),
        ],
    )

    class Meta:
        verbose_name = 'Slugable'
        abstract = True


class NormalizedName(Nameable):
    """Abstract model for normalized name."""

    normalized_name = models.CharField(  # noqa: DJ01
        max_length=constances.MAX_NAME_LENGTH,
        editable=False,
        unique=True,
        null=True,
        verbose_name=_('Normalized Name'),
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
