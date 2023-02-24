from django.contrib import admin

from server.apps.catalog.models import CatalogCategory, CatalogItem, CatalogTag

NameField = 'name'


@admin.register(CatalogItem)
class AdminModelItem(admin.ModelAdmin[CatalogItem]):
    """Views for item model."""

    list_display = (NameField, 'is_published')
    list_editable = ('is_published',)
    list_display_links = (NameField,)
    filter_horizontal = ('tags',)


@admin.register(CatalogTag)
class AdminModelTag(admin.ModelAdmin[CatalogTag]):
    """Views for tag model."""

    list_display = (NameField,)
    list_display_links = (NameField,)


@admin.register(CatalogCategory)
class AdminModelCategory(admin.ModelAdmin[CatalogCategory]):
    """Views for category model."""

    list_display = (NameField,)
    list_display_links = (NameField,)
