from server.apps.catalog.models import (
    CatalogCategory,
    CatalogItem,
    CatalogTag,
    ImageItem,
)

ItemNameField: str = (
    CatalogItem.name.field.name  # type: ignore[attr-defined]
)
ItemPublishedField: str = (
    CatalogItem.is_published.field.name  # type: ignore[attr-defined]
)
ItemTagsField: str = CatalogItem.tags.field.name
ItemCategoryField: str = (
    CatalogItem.category.field.name
)
ItemImageField: str = (
    CatalogItem.image.field.name
)
ItemDescriptionField: str = (
    CatalogItem.text.field.name  # type: ignore[attr-defined]
)
ItemIsOnMainField: str = (
    CatalogItem.is_on_main.field.name  # type: ignore[attr-defined]
)
ItemGalleyField: str = (
    CatalogItem.gallery.field.name
)

TagNameField: str = (
    CatalogTag.name.field.name  # type: ignore[attr-defined]
)
CategoryNameField: str = (
    CatalogCategory.name.field.name  # type: ignore[attr-defined]
)

ImageItemImageField: str = (
    ImageItem.image.field.name
)
