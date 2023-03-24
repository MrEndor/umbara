import re
from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from django.core import mail
from django.test import Client
from django.urls import reverse
from freezegun import freeze_time
from hypothesis import given
from hypothesis import settings as hypothesis_settings
from hypothesis import strategies
from hypothesis.extra import django

from server.apps.users import models

TEST_PASSWORD = 'test'  # noqa: S105


def _login(
    client: Client,
    username: str,
    password: str,
):
    post_data = {'username': username, 'password': password}

    return client.post(
        reverse('users:login'),
        post_data,
    )


@pytest.mark.django_db(transaction=True)
@given(
    user=django.from_model(
        models.UserWithProfile,
        is_active=strategies.just(True),
        username=strategies.text(
            alphabet=strategies.from_regex('^[a-zA-Z]$', fullmatch=True),
            min_size=10,
        ),
        email=strategies.emails(),
        password=strategies.just(TEST_PASSWORD),
    ),
)
@hypothesis_settings(max_examples=10)
def test_auth_by_username_page(  # noqa: WPS218
    client: Client,
    user: models.UserWithProfile,
):
    """This test ensures that signup page works."""
    user.save()

    response = _login(client, username=user.username, password=TEST_PASSWORD)
    assert response.status_code == HTTPStatus.OK

    models.UserWithProfile.objects.filter(
        username=user.username,
    ).delete()


@pytest.mark.django_db(transaction=True)
@given(
    user=django.from_model(
        models.UserWithProfile,
        is_active=strategies.just(True),
        username=strategies.text(
            alphabet=strategies.from_regex('^[a-zA-Z]$', fullmatch=True),
            min_size=10,
        ),
        email=strategies.emails(),
        password=strategies.just(TEST_PASSWORD),
    ),
)
@hypothesis_settings(max_examples=3)
def test_auth_by_email_page(  # noqa: WPS218
    client: Client,
    user: models.UserWithProfile,
):
    """This test ensures that signup page works."""
    models.UserWithProfile.objects.filter(
        email=user.email,
    ).delete()

    user.save()

    response = _login(client, username=user.email, password=TEST_PASSWORD)
    assert response.status_code == HTTPStatus.OK

    models.UserWithProfile.objects.filter(
        email=user.email,
    ).delete()


@pytest.mark.django_db(transaction=True)
@given(
    user=django.from_model(
        models.UserWithProfile,
        is_active=strategies.just(True),
        username=strategies.text(
            alphabet=strategies.from_regex('^[a-zA-Z]$', fullmatch=True),
            min_size=10,
        ),
        email=strategies.emails(),
        password=strategies.just(TEST_PASSWORD),
    ),
)
@hypothesis_settings(max_examples=10)
def test_lockout_page(  # noqa: WPS218
    client: Client,
    settings,
    user: models.UserWithProfile,
):
    """This test ensures that signup page works."""
    user.save()

    for _ in range(settings.AXES_FAILURE_LIMIT):
        _login(
            client,
            user.username,
            'not-a-password',
        )

    email = mail.outbox.pop()

    activate_url = re.search(  # type: ignore[union-attr]
        r'(?P<url>https?://\S+)',
        email.body,
    ).group('url')

    with freeze_time(datetime.now() + timedelta(hours=1)):
        response = client.get(activate_url)

    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == reverse('users:login')

    models.UserWithProfile.objects.filter(
        username=user.username,
    ).delete()
