from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.users import models, forms

USER_FORM_KEY = 'form'
USERNAME_FIELD = 'username'


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'emails',
    [
        ('tester1@ya.ru', 'tester1@yandex.ru'),
        ('tester2+friends@ya.ru', 'tester2@yandex.ru'),
        ('example.ya.net@ya.ru', 'example-ya-net@yandex.ru'),
        ('example.ya.net@gmail.com', 'exampleyanet@gmail.com')
    ]
)
def test_signup_page(  # noqa: WPS218
    client: Client,
    emails: tuple[str, str],
):
    """This test ensures that signup page works."""

    models.UserWithProfile.objects.filter(
        email=emails[1],
    ).delete()

    response = client.post(
        reverse('users:create_signup'), data={
            'username': 'test',
            'password1': 'test',
            'password2': 'test',
            'email': emails[0],
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == reverse('users:login')

    post_data = {'username': emails[1], 'password': 'test'}

    response = client.post(
        reverse('users:login'),
        post_data,
    )
    assert response.status_code == HTTPStatus.OK

    models.UserWithProfile.objects.filter(
        email=emails[1],
    ).delete()
