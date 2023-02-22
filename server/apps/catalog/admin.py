from django.contrib import admin

from server.apps.catalog.models import CatalogCategory, CatalogItem, CatalogTag

NAME_FIELD = 'name'


@admin.register(CatalogItem)
class AdminModelItem(admin.ModelAdmin[CatalogItem]):
    """Views for item model."""

    list_display = (NAME_FIELD, 'is_published')
    list_editable = ('is_published',)
    list_display_links = (NAME_FIELD,)
    filter_horizontal = ('tags',)


@admin.register(CatalogTag)
class AdminModelTag(admin.ModelAdmin[CatalogTag]):
    """Views for tag model."""

    list_display = (NAME_FIELD,)
    list_display_links = (NAME_FIELD,)


@admin.register(CatalogCategory)
class AdminModelCategory(admin.ModelAdmin[CatalogCategory]):
    """Views for category model."""

    list_display = (NAME_FIELD,)
    list_display_links = (NAME_FIELD,)
