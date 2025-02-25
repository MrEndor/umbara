from http import HTTPStatus

from django.test.client import Client
from django.urls import reverse


def test_description_page(client: Client):
    """This test ensures that description page works."""
    response = client.get(reverse('about:description'))

    assert response.status_code == HTTPStatus.OK
