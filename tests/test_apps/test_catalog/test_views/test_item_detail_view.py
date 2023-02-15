from http import HTTPStatus

from django.test.client import Client
from django.urls import reverse
from hypothesis import given, strategies

NegativeNumbers = strategies.integers(max_value=-1)
PositiveNumbersAndNol = strategies.integers(min_value=0)


@given(catalog_id=PositiveNumbersAndNol)
def test_ok_item_detail_page(
    client: Client,
    catalog_item_detail_body: str,
    catalog_id: int,
):
    """This test ensures that item detail page works."""
    response = client.get(reverse('catalog:item_detail', args=(catalog_id,)))

    assert response.status_code == HTTPStatus.OK
    assert response.content.decode() == catalog_item_detail_body


@given(catalog_id=NegativeNumbers)
def test_not_found_item_detail_page(
    client: Client,
    catalog_item_detail_body: str,
    catalog_id: int,
):
    """This test ensures that item detail page get 404."""
    response = client.get('catalog/{catalog_id}'.format(catalog_id=catalog_id))

    assert response.status_code == HTTPStatus.NOT_FOUND


@given(catalog_id=strategies.text())
def test_text_item_detail_page(
    client: Client,
    catalog_item_detail_body: str,
    catalog_id: str,
):
    """This test ensures that item detail page get 404."""
    response = client.get('catalog/{catalog_id}'.format(catalog_id=catalog_id))

    assert response.status_code == HTTPStatus.NOT_FOUND
