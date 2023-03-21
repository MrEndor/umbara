from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

from server.apps.users import fields, models


class UserForm(forms.ModelForm[models.User]):
    """User form."""

    class Meta:
        model = models.User
        verbose_name = _('user form')
        verbose_name_plural = _('feedbacks forms')
        help_texts = {
            fields.EmailFieldUser: 'example@example.com',
        }
        labels = {
            fields.EmailFieldUser: _('Your email'),
        }
        fields = (
            fields.FirstNameFieldUser,
            fields.LastNameFieldUser,
            fields.EmailFieldUser,
            fields.UserNameFieldUser,
        )


class ProfileForm(forms.ModelForm[models.Profile]):
    """Profile form."""

    coffee_count = forms.IntegerField(
        disabled=True,
    )
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
        help_text=_('Your birthday'),
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={'type': 'file'},
        ),
        label=_('Image'),
    )

    class Meta:
        model = models.Profile
        verbose_name = _('profile form')
        verbose_name_plural = _('profiles forms')
        fields = (
            fields.ImageFieldProfile,
            fields.BirthdayFieldProfile,
            fields.CoffeeCountFieldProfile,
        )


class UserCreationForm(auth_forms.UserCreationForm[models.User]):
    """User creation form."""

    email = forms.EmailField(
        help_text='example@example.com',
        label=_('Your email'),
    )

    def save(self, commit: bool = True) -> models.User:
        """Method for save User model with email."""
        self.instance.email = self.cleaned_data['email']
        return super().save(commit)
