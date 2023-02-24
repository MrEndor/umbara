from django.core import validators
from django.db import models

from server.apps.catalog import constants
from server.apps.core.base_models import BaseModel, Slugable


class CatalogCategory(
    BaseModel,
    Slugable,
):
    """Base Category Model."""

    weight = models.IntegerField(
        default=constants.CATEGORY_DEFAULT_WEIGHT,
        validators=[
            validators.MinValueValidator(constants.CATEGORY_WEIGHT_MIN),
            validators.MaxValueValidator(constants.CATEGORY_WEIGHT_MAX),
        ],
        verbose_name='вес',
        help_text='Вес должен быть больше {minimum} и меньше {maximum}'.format(
            minimum=constants.CATEGORY_WEIGHT_MIN,
            maximum=constants.CATEGORY_WEIGHT_MAX,
        ),
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
