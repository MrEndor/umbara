from crispy_forms import helper, layout
from django import forms
from django.utils.translation import gettext_lazy as _

from server.apps.feedback import fields, models


class FeedbackForm(forms.ModelForm[models.Feedback]):
    """Feedback form."""

    feedback_files = forms.FileField(  # noqa: WPS110
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
            },
        ),
    )

    email = forms.EmailField(
        required=True,
        label=_('Your email'),
        help_text='example@example.com',
    )

    viewer = helper.FormHelper()
    viewer.help_text_inline = True
    viewer.layout = layout.Layout(
        'email',
        fields.FeedbackTextField,
        'feedback_files',
    )

    def save(self, commit=True) -> models.Feedback:
        """Method for save Feedback model with personal data."""
        cleaned_data = self.clean()

        if not cleaned_data:
            return super().save(commit)  # pragma: no cover

        personal_data = models.FeedbackPersonalData.objects.get_or_create(
            email=cleaned_data['email'],
        )[0]
        self.instance.personal_data = personal_data

        return super().save(commit)

    def save_m2m(self) -> None:
        """Method for save feedback_files."""
        for uploaded_file in self.files.getlist('feedback_files'):
            feedback_file = models.FeedbackFile.objects.create(
                file=uploaded_file,
                feedback=self.instance,
            )
            self.instance.files.add(feedback_file)

    class Meta:
        model = models.Feedback
        verbose_name = _('feedback form')
        verbose_name_plural = _('feedbacks forms')
        exclude = (
            fields.FeedbackCreateOnField,
            fields.FeedbackStatusField,
            fields.FeedbackFilesField,
            fields.FeedbackPersonalData,
        )
        labels = {
            fields.FeedbackTextField: _('Your message'),
        }
