from typing import TYPE_CHECKING, Optional

from django.db.models import Manager, Prefetch, QuerySet

from server.apps.catalog import models

if TYPE_CHECKING:
    from server.apps.catalog.models import CatalogItem  # pragma: no cover

CatalogName = 'name'
GalleryImage = 'image'
TagsName = 'name'


def get_field_name(
    model_field,
) -> str:
    """Function to get the field name."""
    return model_field.field.name


class CatalogItemManager(Manager['CatalogItem']):
    """Query Manager for CatalogItem."""

    def list_products(self, **extra) -> QuerySet['CatalogItem']:
        """Query for product list page."""
        tags_prefetch = Prefetch(
            get_field_name(self.model.tags),
            queryset=models.CatalogTag.objects.filter(
                is_published=True,
            ).only(
                TagsName,
            ),
        )
        category_prefetch = Prefetch(
            get_field_name(self.model.category),
            queryset=models.CatalogCategory.objects.filter(
                is_published=True,
            ).only(
                CatalogName,
            ),
        )

        return self.filter(
            is_published=True,
            **extra,
        ).prefetch_related(
            tags_prefetch,
            category_prefetch,
        ).defer(
            get_field_name(self.model.is_published),
            get_field_name(self.model.is_on_main),
            get_field_name(self.model.gallery),
        ).order_by(
            get_field_name(self.model.category),
        )

    def get_detail_by(self, pk: int) -> Optional['CatalogItem']:
        """Query for get product."""
        if not self.filter(id=pk, is_published=True).exists():
            return None

        tags_prefetch = Prefetch(
            get_field_name(self.model.tags),
            queryset=models.CatalogTag.objects.filter(
                is_published=True,
            ).only(
                TagsName,
            ),
        )
        category_prefetch = Prefetch(
            get_field_name(self.model.category),
            queryset=models.CatalogCategory.objects.filter(
                is_published=True,
            ).only(
                CatalogName,
            ),
        )
        gallery_prefetch = Prefetch(
            get_field_name(self.model.gallery),
            queryset=models.ImageItem.objects.only(
                GalleryImage,
            ),
        )

        return self.prefetch_related(
            tags_prefetch,
            category_prefetch,
            gallery_prefetch,
        ).defer(
            get_field_name(self.model.is_published),
            get_field_name(self.model.is_on_main),
        ).get(
            id=pk,
        )
