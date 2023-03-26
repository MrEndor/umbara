from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from server.apps.catalog import constants
from server.apps.catalog.logic.queries.item import CatalogItemManager
from server.apps.catalog.models.category import CatalogCategory
from server.apps.catalog.models.tag import CatalogTag
from server.apps.core.models import BaseModel, ImageMixin
from server.apps.core.validators import ContainsValidator

_HELP_TEXT = _(
    'The description should be more than 2x words and ' +
    'contain the words "{words}"',
)


class ImageItem(ImageMixin, models.Model):
    """Image Item Model."""

    product = models.ForeignKey(
        'CatalogItem',
        on_delete=models.CASCADE,
        db_index=True,
    )

    class Meta:
        db_table = 'catalog_images'
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        """Method for string the model."""
        return str(self.image)


# false positive
class CatalogItem(  # type: ignore[misc]
    ImageMixin,
    BaseModel,
):
    """Base Catalog Item Model."""

    text = models.TextField(
        validators=[
            ContainsValidator(
                *constants.CATALOG_ITEM_KEYWORDS,
            ),  # type: ignore[no-untyped-call]
        ],
        verbose_name=_('description'),
        help_text=format_lazy(
            _HELP_TEXT,
            words=', '.join(constants.CATALOG_ITEM_KEYWORDS),
        ),
    )
    tags = models.ManyToManyField(
        CatalogTag,
        verbose_name=_('tags'),
    )
    category = models.ForeignKey(
        CatalogCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('categories'),
    )
    is_on_main = models.BooleanField(
        default=False,
        verbose_name=_('is on main'),
    )
    gallery = models.ManyToManyField(
        ImageItem,
        verbose_name=_('gallery'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = CatalogItemManager()

    class Meta:
        db_table = 'catalog_item'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
