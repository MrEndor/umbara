from http import HTTPStatus

from django.test.client import Client
from django.urls import reverse


def test_home_page(client: Client, homepage_body: str):
    """This test ensures that home page works."""
    response = client.get(reverse('homepage:home'))

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == homepage_body
