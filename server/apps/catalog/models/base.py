from server.apps.core.base_models import Identifiable, Nameable, Publishable


class BaseModel(
    Identifiable,
    Nameable,
    Publishable,
):
    """Base Catalog model."""

    class Meta:
        verbose_name = 'BaseModel'
        abstract = True
