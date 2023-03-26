from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from server.apps.users import fields, models


class UserForm(forms.ModelForm[models.UserWithProfile]):
    """User form."""

    class Meta:
        model = models.UserWithProfile
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

    def clean_email(self):
        """Method for clean email."""
        email = self.cleaned_data.get('email')
        return models.UserWithProfile.objects.normalize_email(
            email=email,
        )


class ProfileForm(forms.ModelForm[models.Profile]):
    """Profile form."""

    coffee_count = forms.IntegerField(
        disabled=True,
    )
    birthday = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            },
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


class UserCreationForm(auth_forms.UserCreationForm[models.UserWithProfile]):
    """User creation form."""

    email = forms.EmailField(
        help_text='example@example.com',
        label=_('Your email'),
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = models.UserWithProfile

    def clean_email(self):
        """Method for clean email."""
        email = self.cleaned_data.get('email')
        user_query = models.UserWithProfile.objects.filter(
            email=email,
        )
        if user_query.exists():
            raise ValidationError(
                _('User with this email already exists'),
            )
        return models.UserWithProfile.objects.normalize_email(
            email=email,
        )

    def save(self, commit: bool = True) -> models.UserWithProfile:
        """Method for save User model with email."""
        self.instance.email = self.cleaned_data['email']
        user = super().save(commit)
        user.create_profile()
        return user


class LoginForm(auth_forms.AuthenticationForm):
    """Login form."""

    username = forms.CharField(
        label=_('Email / Username'),
        widget=forms.TextInput(
            attrs={'autofocus': True},
        ),
    )

    def clean_username(self):
        """Method for clean username."""
        email = self.cleaned_data.get('username')
        return models.UserWithProfile.objects.normalize_email(
            email=email,
        )
