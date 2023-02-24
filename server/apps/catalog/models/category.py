from django.core import validators
from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from server.apps.catalog import constants
from server.apps.core.base_models import NormalizedName, Slugable

WEIGHT_HELP_TEXT = _(
    'Weight must be greater than {minimum} and less than {maximum}',
)


class CatalogCategory(
    NormalizedName,
    Slugable,
):
    """Base Category Model."""

    weight = models.IntegerField(
        default=constants.CATEGORY_DEFAULT_WEIGHT,
        validators=[
            validators.MinValueValidator(constants.CATEGORY_WEIGHT_MIN),
            validators.MaxValueValidator(constants.CATEGORY_WEIGHT_MAX),
        ],
        verbose_name=_('Weight'),
        help_text=format_lazy(
            WEIGHT_HELP_TEXT,
            minimum=constants.CATEGORY_WEIGHT_MIN,
            maximum=constants.CATEGORY_WEIGHT_MAX,
        ),
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
