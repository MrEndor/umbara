from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse
from hypothesis import given, settings

from tests.strategies.catalog import base_item_strategy


@pytest.mark.django_db(transaction=True)
@given(
    product=base_item_strategy,
)
@settings(max_examples=1)
def test_item_list_page(
    client: Client,
    item_list_not_deferred_fields,
    product,
):
    """This test ensures that item list page works."""
    response = client.get(reverse('catalog:item_list'))
    page_key = 'product_page'

    assert page_key in response.context

    product_page = response.context[page_key]
    assert product_page
    assert response.status_code == HTTPStatus.OK

    for product_context in product_page:
        deferred_fields = product_context.get_deferred_fields()

        assert deferred_fields not in item_list_not_deferred_fields


@pytest.mark.django_db(transaction=True)
def test_page_not_found_item_list_page(client: Client):
    """This test ensures that item list page raise 404."""
    response = client.get('/catalog/?page=10')

    assert response.status_code == HTTPStatus.NOT_FOUND
