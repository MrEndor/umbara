from django.db import models

from server.apps.catalog import constances
from server.apps.catalog.models.base import BaseModel
from server.apps.catalog.models.category import CatalogCategory
from server.apps.catalog.models.tag import CatalogTag
from server.apps.core.validators import is_contains

_HELP_TEXT = """
Описание должно быть больше чем из 2x слов и содержать слова "{words}"
"""


class CatalogItem(
    BaseModel,
):
    """Base Catalog Item Model."""

    text = models.TextField(
        validators=[
            is_contains(*constances.CATALOG_ITEM_KEYWORDS),
        ],
        verbose_name='Описание',
        help_text=_HELP_TEXT.format(
            words=', '.join(constances.CATALOG_ITEM_KEYWORDS),
        ),
    )
    tags = models.ManyToManyField(
        CatalogTag,
        verbose_name='Теги',
    )
    category = models.ForeignKey(
        CatalogCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категории',
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
