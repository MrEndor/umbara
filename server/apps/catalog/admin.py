from django.contrib import admin

from server.apps.catalog.models import CatalogCategory, CatalogItem, CatalogTag

CatalogItemNameField: str = (
    CatalogItem.name.field.name  # type: ignore[attr-defined]
)
CatalogItemPublishedField: str = (
    CatalogItem.is_published.field.name  # type: ignore[attr-defined]
)
CatalogItemTagsField: str = CatalogItem.tags.field.name

CatalogTagNameField: str = (
    CatalogTag.name.field.name  # type: ignore[attr-defined]
)
CatalogCategoryField: str = (
    CatalogTag.name.field.name  # type: ignore[attr-defined]
)


@admin.register(CatalogItem)
class AdminModelItem(admin.ModelAdmin[CatalogItem]):
    """Views for item model."""

    list_display = (
        CatalogItemNameField,
        CatalogItemPublishedField,
    )
    list_editable = (CatalogItemPublishedField,)
    list_display_links = (CatalogItemNameField,)
    filter_horizontal = (CatalogItemTagsField,)


@admin.register(CatalogTag)
class AdminModelTag(admin.ModelAdmin[CatalogTag]):
    """Views for tag model."""

    list_display = (CatalogTagNameField,)
    list_display_links = (CatalogTagNameField,)


@admin.register(CatalogCategory)
class AdminModelCategory(admin.ModelAdmin[CatalogCategory]):
    """Views for category model."""

    list_display = (CatalogCategoryField,)
    list_display_links = (CatalogCategoryField,)
