from django.core import validators
from django.db import models

from server.apps.core import constants


class BaseModel(models.Model):
    """Base model."""

    name = models.CharField(
        max_length=constants.MAX_NAME_LENGTH,
        verbose_name='название',
        help_text='Максимальная длина {maximum}'.format(
            maximum=constants.MAX_NAME_LENGTH,
        ),
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='опубликовано',
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
