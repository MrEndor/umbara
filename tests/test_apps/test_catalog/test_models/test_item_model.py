from random import choice, randrange
from typing import List

import pytest
from django.core.exceptions import ValidationError
from hypothesis import given, settings, strategies
from hypothesis.extra import django

from server.apps.catalog.constants import CATALOG_ITEM_KEYWORDS
from server.apps.catalog.models import CatalogCategory, CatalogItem, CatalogTag


@strategies.composite
def _item_text_strategies(draw):
    """Keyword Text Generation Strategy."""
    text: List[str] = draw(strategies.text(min_size=2)).split()
    word = choice(CATALOG_ITEM_KEYWORDS)  # noqa: S311

    text.insert(
        randrange(0, len(text)),  # noqa: S311
        word,
    )

    return ''.join(text)


def include_tags(
    product: CatalogItem, tags: List[CatalogTag],
) -> CatalogItem:
    """Function to add tags."""
    product.tags.add(*tags)

    return product


def generate_product_with_tags(
    products: strategies.SearchStrategy[CatalogItem],
) -> strategies.SearchStrategy[CatalogItem]:
    """Strategy for Generating a Tagged Product."""
    return strategies.builds(
        include_tags,
        products,
        base_tags_strategy,
    )


base_tags_strategy = strategies.lists(
    django.from_model(
        CatalogTag,
        id=strategies.integers(
            min_value=1,
            max_value=(2 ** 63) - 1,
        ),
    ),
    min_size=1,
    unique=True,
)

base_category_strategy = django.from_model(
    CatalogCategory,
    id=strategies.integers(
        min_value=1,
        max_value=(2 ** 63) - 1,
    ),
)


class TestItemModel(django.TestCase):
    """Class for product testing."""

    @given(
        generate_product_with_tags(
            django.from_model(
                CatalogItem,
                category=base_category_strategy,
                text=_item_text_strategies(),
            ),
        ),
    )
    @settings(max_examples=1)
    def test_item_model_properties(self, instance: CatalogItem):
        """This test verifies the overall ownership of the data."""
        instance.save()

        assert instance.id > 0
        assert instance.tags.exists()
        assert instance.category
        assert len(instance.name) <= 150
        assert isinstance(instance.is_published, bool)

    @given(
        django.from_model(
            CatalogItem,
            name=strategies.text(min_size=151),
            category=base_category_strategy,
            text=_item_text_strategies(),
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
