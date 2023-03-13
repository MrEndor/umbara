from crispy_forms import helper, layout
from django import forms
from django.utils.translation import gettext_lazy as _

from server.apps.feedback import models


class FeedbackForm(forms.ModelForm[models.Feedback]):
    """Feedback form."""

    viewer = helper.FormHelper()
    viewer.help_text_inline = True
    viewer.layout = layout.Layout(
        layout.Row(
            layout.Column(
                'email',
                css_class='form-group col-md-9 mb-0',
            ),
            css_class='form-row',
        ),
        'text',
        layout.Submit('submit', _('Submit')),
    )

    class Meta:
        model = models.Feedback
        verbose_name = _('feedback form')
        verbose_name_plural = _('feedbacks forms')
        exclude = (
            models.Feedback.created_on.field.name,  # type: ignore[attr-defined]
        )
        labels = {
            'email': _('Your email'),
            'text': _('Your message'),
        }
        help_texts = {
            'email': 'example@example.com',
        }
