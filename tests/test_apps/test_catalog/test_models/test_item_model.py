import pytest
from django.core.exceptions import ValidationError
from hypothesis import given, settings, strategies
from hypothesis.extra import django

from server.apps.catalog.models import CatalogItem, CatalogTag
from tests.strategies.catalog import (
    base_category_strategy,
    base_item_strategy,
    item_text_strategies,
)


class TestItemModel(django.TestCase):
    """Class for product testing."""

    @given(
        base_item_strategy,
    )
    @settings(max_examples=1)
    def test_item_model_properties(self, instance: CatalogItem):  # noqa: WPS218
        """This test verifies the overall ownership of the data."""
        instance.save()

        assert instance.id > 0
        assert instance.tags.exists()
        assert instance.category
        assert len(instance.name) <= 150
        assert isinstance(instance.is_published, bool)
        assert instance.images
        assert len(str(instance.images[0]))
        assert len(str(instance))

    @given(
        django.from_model(
            CatalogItem,
            name=strategies.text(min_size=151),
            category=base_category_strategy,
            text=item_text_strategies(),
        ),
    )
    @settings(max_examples=2)
    def test_raise_item_model_name_properties(self, instance: CatalogTag):
        """The test checks the validity of the product name."""
        with pytest.raises(
            ValidationError,
            match='Ensure this value has at most 150 characters',
        ):
            instance.full_clean()

        assert len(instance.name) > 150
