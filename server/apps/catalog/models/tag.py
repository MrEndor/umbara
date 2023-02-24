from django.utils.translation import gettext_lazy as _

from server.apps.core.base_models import NormalizedName


class CatalogTag(
    NormalizedName,
):
    """Base Catalog Tag Model."""

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
