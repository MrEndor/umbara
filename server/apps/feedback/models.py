from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.core.models.file import FileMixin
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


class FeedbackPersonalData(models.Model):
    """Model for personal data."""

    email = models.EmailField(
        verbose_name=_('email'),
        unique=True,
    )

    class Meta:
        verbose_name = _('personal data')
        verbose_name_plural = _('personal data')

    def __str__(self):
        """Method for string the model."""
        return str(self.id)  # pragma: no cover


class FeedbackFile(FileMixin):
    """Model feedback file."""

    feedback = models.ForeignKey(
        'Feedback',
        on_delete=models.CASCADE,
        verbose_name=_('feedback'),
    )

    def get_path(self, filename: str) -> str:
        """Function for get file path."""
        return 'uploads/{id}/{filename}'.format(
            id=self.feedback.id, filename=filename,
        )

    class Meta:
        verbose_name = _('feedback file')
        verbose_name_plural = _('feedbacks files')


class Feedback(models.Model):
    """Feedback model."""

    text = models.TextField(
        verbose_name=_('text'),
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.CharField(
        choices=EmailStatus.CHOICES,
        default=EmailStatus.RECEIVED,
        max_length=constants.MAX_STATUS_LENGTH,
        verbose_name=_('status'),
    )
    files = models.ManyToManyField(
        FeedbackFile,
        verbose_name=_('files'),
        related_name='files',
    )
    personal_data = models.ForeignKey(
        FeedbackPersonalData,
        verbose_name=_('personal data'),
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = _('feedback form')
        verbose_name_plural = _('feedbacks forms')

    def __str__(self):
        """Method for string the model."""
        return str(self.created_on)
