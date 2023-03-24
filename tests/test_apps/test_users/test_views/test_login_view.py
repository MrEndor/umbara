from http import HTTPStatus
from freezegun import freeze_time
from datetime import datetime, timedelta

import re
import pytest
from django.core import mail
from django.test import Client
from django.urls import reverse
from hypothesis import given, settings, strategies
from hypothesis.extra import django

from server.apps.users import models


def _login(client, username, password):
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
        username=strategies.from_regex('^[a-zA-Z]$', fullmatch=True),
        email=strategies.emails(),
        password=strategies.just('test')
    )
)
@settings(max_examples=10)
def test_login_page(  # noqa: WPS218
    client: Client,
    user: models.UserWithProfile,
):
    """This test ensures that signup page works."""
    user.save()
    form_data = {'username': user.username, 'password': 'test'}

    response = client.get(reverse('users:login'), data=form_data)
    assert response.status_code == HTTPStatus.OK

    client.logout()

    form_data = {'username': user.email, 'password': 'test'}

    response = client.get(reverse('users:login'), data=form_data)
    assert response.status_code == HTTPStatus.OK

    user.delete()


@pytest.mark.django_db(transaction=True)
@given(
    user=django.from_model(
        models.UserWithProfile,
        is_active=strategies.just(True),
        username=strategies.from_regex('^[a-zA-Z]$', fullmatch=True),
        email=strategies.emails(),
        password=strategies.just('test')
    )
)
@settings(max_examples=10)
def test_login_page(  # noqa: WPS218
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
