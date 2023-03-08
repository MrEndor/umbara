from django.contrib import admin

from server.apps.catalog import forms
from server.apps.catalog.models import (
    CatalogCategory,
    CatalogItem,
    CatalogTag,
    ImageItem,
    fields,
)

admin.site.register(ImageItem)


class InlineGalleryAdmin(
    admin.TabularInline[ImageItem, CatalogItem],
):
    """Views for gallery model."""

    model = ImageItem
    extra = 1
    form = forms.ImageItemAdminForm


@admin.register(CatalogItem)
class AdminModelItem(admin.ModelAdmin[CatalogItem]):
    """Views for item model."""

    list_display = (
        fields.ItemNameField,
        fields.ItemPublishedField,
        fields.ItemIsOnMainField,
        CatalogItem.view_image,
    )
    list_editable = (fields.ItemPublishedField, fields.ItemIsOnMainField)
    list_display_links = (fields.ItemNameField,)
    filter_horizontal = (fields.ItemTagsField,)
    inlines = (InlineGalleryAdmin,)
    exclude = (fields.ItemGalleyField,)
    form = forms.CatalogItemAdminForm


@admin.register(CatalogTag)
class AdminModelTag(admin.ModelAdmin[CatalogTag]):
    """Views for tag model."""

    list_display = (fields.TagNameField,)
    list_display_links = (fields.TagNameField,)


@admin.register(CatalogCategory)
class AdminModelCategory(admin.ModelAdmin[CatalogCategory]):
    """Views for category model."""

    list_display = (fields.CategoryNameField,)
    list_display_links = (fields.CategoryNameField,)
