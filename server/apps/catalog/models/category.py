from django.core import validators
from django.db import models

from server.apps.catalog import constances
from server.apps.catalog.models.base import BaseModel
from server.apps.core.base_models import Slugable


class CatalogCategory(
    BaseModel,
    Slugable,
):
    """Base Category Model."""

    weight = models.IntegerField(
        default=constances.CATEGORY_DEFAULT_WEIGHT,
        validators=[
            validators.MinValueValidator(constances.CATEGORY_WEIGHT_MIN),
            validators.MaxValueValidator(constances.CATEGORY_WEIGHT_MAX),
        ],
        verbose_name='Вес',
        help_text='Вес должен быть больше {minimum} и меньше {maximum}'.format(
            minimum=constances.CATEGORY_WEIGHT_MIN,
            maximum=constances.CATEGORY_WEIGHT_MAX,
        ),
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
