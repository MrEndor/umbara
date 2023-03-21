from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter(is_safe=False)
def unspecified(field):  # pragma: no cover
    """Template tag for change string to 'unspecified'."""
    if field:
        return field

    return mark_safe(  # noqa: S703 S308
        '<span style="font-weight: bold;">{text}</span>'.format(
            text=_('unspecified'),
        ),
    )
