from typing import Optional

from django.db.models import Prefetch, QuerySet

from server.apps.catalog.models import (
    CatalogCategory,
    CatalogItem,
    CatalogTag,
    ImageItem,
    fields,
)


def all_on_main() -> QuerySet[CatalogItem]:
    """Query for main page."""
    tags_prefetch = Prefetch(
        fields.ItemTagsField,
        queryset=CatalogTag.objects.filter(
            is_published=True,
        ).only(
            fields.TagNameField,
        ),
    )
    category_prefetch = Prefetch(
        fields.ItemCategoryField,
        queryset=CatalogCategory.objects.filter(
            is_published=True,
        ).only(
            fields.CategoryNameField,
        ),
    )

    return CatalogItem.objects.filter(
        is_on_main=True,
        is_published=True,
    ).order_by(
        fields.ItemNameField,
    ).prefetch_related(
        tags_prefetch,
        category_prefetch,
    ).only(
        fields.ItemNameField,
        fields.ItemDescriptionField,
        fields.ItemCategoryField,
        fields.ItemTagsField,
        fields.ItemImageField,
    )


def list_products() -> QuerySet[CatalogItem]:
    """Query for main page."""
    tags_prefetch = Prefetch(
        fields.ItemTagsField,
        queryset=CatalogTag.objects.filter(
            is_published=True,
        ).only(
            fields.TagNameField,
        ),
    )
    category_prefetch = Prefetch(
        fields.ItemCategoryField,
        queryset=CatalogCategory.objects.filter(
            is_published=True,
        ).only(
            fields.CategoryNameField,
        ),
    )

    return CatalogItem.objects.filter(
        is_published=True,
    ).order_by(
        fields.ItemCategoryField,
    ).prefetch_related(
        tags_prefetch,
        category_prefetch,
    ).only(
        fields.ItemNameField,
        fields.ItemDescriptionField,
        fields.ItemCategoryField,
        fields.ItemTagsField,
        fields.ItemImageField,
    )


def get_detail_by(pk: int) -> Optional[CatalogItem]:
    """Query for main page."""
    if not CatalogItem.objects.filter(id=pk, is_published=True).exists():
        return None

    tags_prefetch = Prefetch(
        fields.ItemTagsField,
        queryset=CatalogTag.objects.filter(
            is_published=True,
        ).only(
            fields.TagNameField,
        ),
    )
    category_prefetch = Prefetch(
        fields.ItemCategoryField,
        queryset=CatalogCategory.objects.filter(
            is_published=True,
        ).only(
            fields.CategoryNameField,
        ),
    )
    gallery_prefetch = Prefetch(
        fields.ItemGalleyField,
        queryset=ImageItem.objects.only(
            fields.ImageItemImageField,
        ),
    )

    return CatalogItem.objects.prefetch_related(
        tags_prefetch,
        category_prefetch,
        gallery_prefetch,
    ).only(
        fields.ItemNameField,
        fields.ItemDescriptionField,
        fields.ItemCategoryField,
        fields.ItemTagsField,
        fields.ItemImageField,
    ).get(id=pk)
