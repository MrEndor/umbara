import re
from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from django.core import mail
from django.test import Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time
from hypothesis import given, settings

from server.apps.users.forms import UserCreationForm, UserForm
from server.apps.users.models import User
from tests.strategies.user import base_user_signup_form_strategy

USER_FORM_KEY = 'form'
USERNAME_FIELD = 'username'


@pytest.mark.django_db()
def test_signup_page(  # noqa: WPS218
    client: Client,
):
    """This test ensures that signup page works."""
    response = client.get(reverse('users:signup'))

    assert USER_FORM_KEY in response.context
    form: UserForm = response.context[USER_FORM_KEY]

    email_field = form.fields['email']
    password1_field = form.fields['password1']
    password2_field = form.fields['password2']

    assert email_field.help_text == 'example@example.com'
    assert email_field.label == _('Your email')
    assert password1_field.label == _('Password')
    assert password2_field.label == _('Password confirmation')
    assert USERNAME_FIELD in form.fields


@pytest.mark.django_db()
@given(
    form=base_user_signup_form_strategy,
)
@settings(max_examples=10)
def test_signup_create_page(  # noqa: WPS218
    client: Client,
    form: UserCreationForm,
):
    """This test ensures that signup create page works."""
    fields = form.data

    response = client.post(
        reverse('users:create_signup'), data=fields,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == reverse('users:login')

    user_query = User.objects.filter(
        username=fields[USERNAME_FIELD],
    )
    assert user_query.exists()
    user: User = user_query.get()
    assert user.profile  # type: ignore[attr-defined]
    assert not user.is_active
    assert not user.is_staff
    assert not user.is_superuser

    user_query.delete()


@pytest.mark.django_db(transaction=True)
@given(
    form=base_user_signup_form_strategy,
)
@settings(max_examples=10)
def test_active_create_page(  # noqa: WPS210
    client: Client,
    form: UserCreationForm,
):
    """This test ensures that activate page works."""
    fields = form.data

    User.objects.filter(username=fields[USERNAME_FIELD]).delete()

    now = datetime.now() + timedelta(hours=12)

    response = client.post(
        reverse('users:create_signup'), data=fields,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == reverse('users:login')

    email = mail.outbox.pop()

    activate_url = re.search(  # type: ignore[union-attr]
        r'(?P<url>https?://\S+)',
        email.body,
    ).group('url')

    with freeze_time(now):
        response = client.get(activate_url)

    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == reverse('users:activate_done')

    user = User.objects.get(username=fields['username'])

    assert user.is_active

    user.delete()


@pytest.mark.django_db(transaction=True)
def test_error_signup_create_page(client: Client):
    """This test ensures that feedback create page raise 400."""
    response = client.post(
        reverse('users:create_signup'),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
