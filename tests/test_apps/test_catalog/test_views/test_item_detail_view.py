from http import HTTPStatus

from django.test.client import Client
from django.urls import reverse


def test_item_detail_page(client: Client, catalog_item_detail_body):
    """This test ensures that item detail page works."""
    response = client.get(reverse('catalog:item_detail', args=(1, )))

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == catalog_item_detail_body
