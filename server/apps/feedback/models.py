from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.feedback import constants


class EmailStatus:
    """Statuses for feedback."""

    RECEIVED = 'received'  # noqa: WPS115
    PROCESSING = 'in_processing'  # noqa: WPS115
    ANSWER_GIVEN = 'answer_given'  # noqa: WPS115

    CHOICES = [  # noqa: WPS115
        (RECEIVED, _('Received')),
        (PROCESSING, _('In processing')),
        (ANSWER_GIVEN, _('The answer is given')),
    ]


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
    status = models.CharField(
        choices=EmailStatus.CHOICES,
        default=EmailStatus.RECEIVED,
        max_length=constants.MAX_STATUS_LENGTH,
        verbose_name=_('status'),
    )

    class Meta:
        verbose_name = _('feedback form')
        verbose_name_plural = _('feedbacks forms')

    def __str__(self):
        """Method for string the model."""
        return str(self.created_on)
