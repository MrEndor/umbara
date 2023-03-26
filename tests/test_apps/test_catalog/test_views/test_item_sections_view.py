import datetime
from http import HTTPStatus

import mock
import pytest
from django.urls import reverse
from hypothesis import given, settings
from hypothesis.extra import django

from server.apps.catalog.models import CatalogItem
from tests.strategies.catalog import base_item_strategy

SECTION_KEY = 'section'
PAGE_KEY = 'product_page'


@pytest.mark.usefixtures('item_list_not_deferred_fields', 'client')
class TestSections(django.TransactionTestCase):
    """Class for testing sections pages."""

    @given(product=base_item_strategy)
    @settings(max_examples=1)
    def test_item_new_products_page(
        self,
        product: CatalogItem,
    ):
        """This test ensures that item detail page works."""
        response = self.client.get(reverse('catalog:item_new_products'))

        assert PAGE_KEY in response.context
        assert SECTION_KEY in response.context

        product_page = response.context[PAGE_KEY]
        assert product_page.count() > 0
        assert response.status_code == HTTPStatus.OK

        for product_context in product_page:
            deferred_fields = product_context.get_deferred_fields()

            assert deferred_fields not in self.item_list_not_deferred_fields

    @given(product=base_item_strategy)
    @settings(max_examples=1)
    def test_ok_old_products_page(
        self,
        product: CatalogItem,
    ):
        """This test ensures that item detail page works."""
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = product.created_at
            product.save()

        response = self.client.get(reverse('catalog:item_old_products'))

        assert PAGE_KEY in response.context
        assert SECTION_KEY in response.context

        product_page = response.context[PAGE_KEY]

        assert product_page
        assert response.status_code == HTTPStatus.OK

        for product_context in product_page:
            deferred_fields = product_context.get_deferred_fields()

            assert deferred_fields not in self.item_list_not_deferred_fields

    @given(product=base_item_strategy)
    @settings(max_examples=1)
    def test_ok_friday_products_page(
        self,
        product: CatalogItem,
    ):
        """This test ensures that item detail page works."""
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime.date(
                2023, 3, 10,
            )
            product.save()

        response = self.client.get(reverse('catalog:item_friday_products'))

        assert PAGE_KEY in response.context
        assert SECTION_KEY in response.context

        product_page = response.context[PAGE_KEY]
        assert product_page.count() > 0
        assert response.status_code == HTTPStatus.OK

        for product_context in product_page:
            deferred_fields = product_context.get_deferred_fields()

            assert deferred_fields not in self.item_list_not_deferred_fields

    @pytest.fixture(autouse=True)
    def _item_list_not_deferred_fields(
        self,
        item_list_not_deferred_fields,
    ):
        self.item_list_not_deferred_fields = item_list_not_deferred_fields
