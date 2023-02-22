from django.core import validators
from django.db import models

from server.apps.core import constances


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
        verbose_name='Название',
        help_text='Максимальная длина {maximum}'.format(
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
        verbose_name='Опубликовано',
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
