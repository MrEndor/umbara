from http import HTTPStatus

import pytest
from django.contrib.auth import models as auth_models
from django.test import Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from hypothesis import given, settings, strategies
from hypothesis.extra import django

from server.apps.users import forms, models


@pytest.mark.django_db(transaction=True)
@given(
    profile=django.from_model(
        models.Profile,
        user=django.from_model(
            auth_models.User,
            is_active=strategies.just(True),
        ),
    ),
)
@settings(max_examples=10)
def test_profile_page(  # noqa: WPS218
    client: Client,
    profile: models.Profile,
):
    """This test ensures that profile page works."""
    client.force_login(profile.user)
    response = client.get(reverse('users:profile'))

    assert response.status_code == HTTPStatus.OK

    assert 'user_form' in response.context
    assert 'profile_form' in response.context

    user_form: forms.UserForm = response.context['user_form']
    profile_form: forms.ProfileForm = response.context['profile_form']

    email_field = user_form.fields['email']
    image_field = profile_form.fields['image']

    assert email_field.help_text == 'example@example.com'
    assert email_field.label == _('Your email')
    assert image_field.label == _('Image')

    profile.user.delete()


@pytest.mark.django_db(transaction=True)
@given(
    profile_form=django.from_form(
        forms.ProfileForm,  # type: ignore[arg-type] #
        coffee_count=strategies.integers(min_value=0, max_value=100),
        image=strategies.binary(min_size=100),
    ),
    user_form=django.from_form(
        forms.UserForm,  # type: ignore[arg-type]
        username=strategies.text(
            alphabet=strategies.from_regex(
                '^[a-zA-Z]$', fullmatch=True,
            ),
            min_size=10,
            max_size=150,
        ),
        email=strategies.emails(),
    ),
)
@settings(max_examples=10)
def test_profile_change_page(
    client: Client,
    profile_form: forms.ProfileForm,
    user_form: forms.UserForm,
):
    """This test ensures that profile page works."""
    assert user_form.is_valid()

    user = user_form.save()

    profile = profile_form.instance
    profile.user = user
    profile.save()

    client.force_login(user)

    fields = dict(profile_form.data) | dict(user_form.data)

    response = client.post(
        reverse('users:change_profile'), data=fields,
    )

    assert response.status_code == HTTPStatus.OK

    client.logout()

    user.delete()


@pytest.mark.django_db(transaction=True)
@given(
    profile=django.from_model(
        models.Profile,
        user=django.from_model(
            models.UserWithProfile,
            is_active=strategies.just(True),
        ),
    ),
)
@settings(max_examples=2)
def test_error_profile_change_page(
    client: Client,
    profile: models.Profile,
):
    """This test ensures that profile change page raise 400."""
    client.force_login(profile.user)
    response = client.post(
        reverse('users:change_profile'),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    profile.user.delete()
