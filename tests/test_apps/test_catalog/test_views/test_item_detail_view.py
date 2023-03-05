from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse
from hypothesis import given, settings, strategies

from server.apps.catalog.models import CatalogItem
from tests.strategies.catalog import base_item_strategy

NegativeNumbers = strategies.integers(max_value=-1)
PositiveNumbersAndNol = strategies.integers(min_value=0)


@pytest.mark.django_db(transaction=True)
@given(product=base_item_strategy)
@settings(max_examples=10)
def test_ok_item_detail_page(
    client: Client,
    product: CatalogItem,
):
    """This test ensures that item detail page works."""
    response = client.get(reverse('catalog:item_detail', args=(product.id,)))

    assert 'product' in response.context
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db(transaction=True)
@given(product_id=NegativeNumbers)
def test_not_found_item_detail_page(
    client: Client,
    product_id: int,
):
    """This test ensures that item detail page get 404."""
    response = client.get('catalog/{product_id}'.format(product_id=product_id))

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db(transaction=True)
@given(product_id=strategies.text())
def test_text_item_detail_page(
    client: Client,
    product_id: str,
):
    """This test ensures that item detail page get 404."""
    response = client.get('catalog/{product_id}'.format(product_id=product_id))

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db()
@given(product=base_item_strategy)
@settings(max_examples=10)
def test_true_statement_regex_url_item_detail(
    client: Client,
    product: CatalogItem,
):
    """This test ensures that regex works."""
    response = client.get(
        '/catalog/re/{product_id}/'.format(product_id=product.id),
    )

    assert 'product' in response.context
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
@given(product=base_item_strategy)
@settings(max_examples=10)
def test_true_statement_converter_url_item_detail(
    client: Client,
    product: CatalogItem,
):
    """This test ensures that converter works."""
    response = client.get(
        reverse('catalog:convert_item_detail', args=(product.id,)),
    )

    assert 'product' in response.context
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
@given(product_id=NegativeNumbers)
def test_false_statement_converter_item_detail(
    client: Client,
    product_id: str,
):
    """This test ensures that converter does not work."""
    response = client.get(
        '/catalog/converter/{product_id}/'.format(product_id=product_id),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db(transaction=True)
def test_page_not_found_item_detail(
    client: Client,
):
    """This test ensures that item detail raise 404."""
    response = client.get(
        '/catalog/10',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
