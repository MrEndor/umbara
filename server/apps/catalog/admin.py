from django.contrib import admin

from server.apps.catalog.forms import CatalogItemAdminForm, ImageItemAdminForm
from server.apps.catalog.models import (
    CatalogCategory,
    CatalogItem,
    CatalogTag,
    ImageItem,
)

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

admin.site.register(ImageItem)


class InlineGalleryAdmin(
    admin.TabularInline[ImageItem, CatalogItem],
):
    """Views for gallery model."""

    model = ImageItem
    extra = 1
    form = ImageItemAdminForm


@admin.register(CatalogItem)
class AdminModelItem(admin.ModelAdmin[CatalogItem]):
    """Views for item model."""

    list_display = (
        CatalogItemNameField,
        CatalogItemPublishedField,
        CatalogItem.view_image,
    )
    list_editable = (CatalogItemPublishedField,)
    list_display_links = (CatalogItemNameField,)
    filter_horizontal = (CatalogItemTagsField,)
    inlines = (InlineGalleryAdmin,)
    form = CatalogItemAdminForm


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
