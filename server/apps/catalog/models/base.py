from server.apps.core.base_models import Identifiable, Publishable


class BaseModel(
    Identifiable,
    Publishable,
):
    """Base Catalog model."""

    class Meta:
        verbose_name = 'BaseModel'
        abstract = True
