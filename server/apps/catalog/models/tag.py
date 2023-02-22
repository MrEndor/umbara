from server.apps.catalog.models.base import BaseModel


class CatalogTag(
    BaseModel,
):
    """Base Catalog Tag Model."""

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
