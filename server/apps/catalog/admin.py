from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin, AdminInlineImageMixin

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
    AdminInlineImageMixin,
    admin.TabularInline[ImageItem, CatalogItem],
):
    """Views for gallery model."""

    model = ImageItem
    extra = 1


@admin.register(CatalogItem)
class AdminModelItem(AdminImageMixin, admin.ModelAdmin[CatalogItem]):
    """Views for item model."""

    list_display = (
        CatalogItemNameField,
        CatalogItemPublishedField,
    )
    list_editable = (CatalogItemPublishedField,)
    list_display_links = (CatalogItemNameField,)
    filter_horizontal = (CatalogItemTagsField,)
    inlines = (InlineGalleryAdmin,)


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
