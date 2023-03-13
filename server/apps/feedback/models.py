from django.db import models
from django.utils.translation import gettext_lazy as _


class Feedback(models.Model):
    """Feedback model."""

    text = models.TextField(
        verbose_name=_('text'),
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
    )
    email = models.EmailField(
        verbose_name=_('email'),
    )

    class Meta:
        verbose_name = _('feedback form')
        verbose_name_plural = _('feedbacks forms')

    def __str__(self):
        """Method for string the model."""
        return str(self.created_on)
