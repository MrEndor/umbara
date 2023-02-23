from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from server.apps.catalog import constances
from server.apps.catalog.models.base import BaseModel
from server.apps.catalog.models.category import CatalogCategory
from server.apps.catalog.models.tag import CatalogTag
from server.apps.core.base_models import Nameable
from server.apps.core.validators import is_contains

_HELP_TEXT = _(
    'The description should be more than 2x words and ' +
    'contain the words "{words}"',
)


class CatalogItem(
    BaseModel,
    Nameable,
):
    """Base Catalog Item Model."""

    text = models.TextField(
        validators=[
            is_contains(*constances.CATALOG_ITEM_KEYWORDS),
        ],
        verbose_name=_('Description'),
        help_text=format_lazy(
            _HELP_TEXT,
            words=', '.join(constances.CATALOG_ITEM_KEYWORDS),
        ),
    )
    tags = models.ManyToManyField(
        CatalogTag,
        verbose_name=_('Tags'),
    )
    category = models.ForeignKey(
        CatalogCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Categories'),
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
