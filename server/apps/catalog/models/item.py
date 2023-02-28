from functools import cached_property

from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from sorl import thumbnail

from server.apps.catalog import constants
from server.apps.catalog.models.category import CatalogCategory
from server.apps.catalog.models.tag import CatalogTag
from server.apps.core.models import BaseModel
from server.apps.core.validators import is_contains

_HELP_TEXT = _(
    'The description should be more than 2x words and ' +
    'contain the words "{words}"',
)


class ImageItem(models.Model):
    """Image Item Model."""

    image = thumbnail.ImageField(
        upload_to='images',
        verbose_name=_('image'),
    )
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
        return '{product}/{image}'.format(
            product=self.product.name,
            image=self.image.name,
        )


class CatalogItem(
    BaseModel,
):
    """Base Catalog Item Model."""

    text = models.TextField(
        validators=[
            is_contains(*constants.CATALOG_ITEM_KEYWORDS),
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
    main_image = thumbnail.ImageField(
        upload_to='catalog_images',
        verbose_name=_('image'),
        null=True,
    )

    @cached_property
    def images(self):
        """Property for all product pictures."""
        return ImageItem.objects.filter(product=self.id).all()

    class Meta:
        db_table = 'catalog_item'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
