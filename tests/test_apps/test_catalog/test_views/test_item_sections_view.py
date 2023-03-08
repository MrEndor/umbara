import datetime
from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse
from hypothesis import given, settings

from server.apps.catalog.models import CatalogItem
from tests.strategies.catalog import base_item_strategy

SECTION_KEY = 'section'


@pytest.mark.django_db(transaction=True)
@given(product=base_item_strategy)
@settings(max_examples=1)
def test_item_new_products_page(
    client: Client,
    item_list_not_deferred_fields,
    product: CatalogItem,
):
    """This test ensures that item detail page works."""
    response = client.get(reverse('catalog:item_new_products'))
    page_key = 'product_page'

    assert page_key in response.context
    assert SECTION_KEY in response.context

    product_page = response.context[page_key]
    assert product_page
    assert response.status_code == HTTPStatus.OK

    for product_context in product_page:
        deferred_fields = product_context.get_deferred_fields()

        assert deferred_fields not in item_list_not_deferred_fields


@pytest.mark.django_db(transaction=True)
@given(product=base_item_strategy)
@settings(max_examples=5)
def test_ok_old_products_page(
    client: Client,
    item_list_not_deferred_fields,
    product: CatalogItem,
):
    """This test ensures that item detail page works."""
    response = client.get(reverse('catalog:item_old_products'))
    page_key = 'product_page'

    assert page_key in response.context
    assert SECTION_KEY in response.context

    product_page = response.context[page_key]
    assert product_page
    assert response.status_code == HTTPStatus.OK

    for product_context in product_page:
        deferred_fields = product_context.get_deferred_fields()

        assert deferred_fields not in item_list_not_deferred_fields


@pytest.mark.django_db(transaction=True)
@given(product=base_item_strategy)
@settings(max_examples=1)
def test_ok_friday_products_page(
    client: Client,
    item_list_not_deferred_fields,
    product: CatalogItem,
):
    """This test ensures that item detail page works."""
    product.updated_at = datetime.date(
        2023, 3, 10,
    )
    response = client.get(reverse('catalog:item_friday_products'))
    page_key = 'product_page'

    assert page_key in response.context
    assert SECTION_KEY in response.context

    product_page = response.context[page_key]
    assert product_page
    assert response.status_code == HTTPStatus.OK

    for product_context in product_page:
        deferred_fields = product_context.get_deferred_fields()

        assert deferred_fields not in item_list_not_deferred_fields
