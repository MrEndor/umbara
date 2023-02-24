import pytest
from django.core.exceptions import ValidationError
from hypothesis import given, settings, strategies
from hypothesis.extra import django

from server.apps.catalog.models import CatalogCategory

SLUG_VALIDATION_TEXT = (
    'Enter a valid “slug” consisting of letters, ' +
    'numbers, underscores or hyphens.'
)


class TestCategoryModel(django.TestCase):
    """Class for testing category model."""

    @given(django.from_model(
        CatalogCategory,
    ))
    @settings(max_examples=10)
    def test_category_model_properties(
        self, instance: CatalogCategory,
    ):
        """This test checks the general operability."""
        instance.save()

        assert instance.id > 0
        assert len(instance.name) <= 150
        assert isinstance(instance.is_published, bool)

    @given(django.from_model(
        CatalogCategory,
        name=strategies.text(min_size=151),
    ))
    @settings(max_examples=10)
    def test_raise_category_model_name_properties(
        self, instance: CatalogCategory,
    ):
        """This test checks the validity of the name category."""
        with pytest.raises(
            ValidationError,
            match='Ensure this value has at most 150 characters',
        ):
            instance.full_clean()

        assert len(instance.name) > 150

    @given(django.from_model(
        CatalogCategory,
        slug=strategies.from_regex(
            '[а-яА-Я?:%;№"!)(*&<>,.]',
        ),
    ))
    @settings(max_examples=10)
    def test_raise_category_model_slug_properties(
        self, instance: CatalogCategory,
    ):
        """This test checks the validity of the slug category."""
        with pytest.raises(
            ValidationError,
            match=SLUG_VALIDATION_TEXT,
        ):
            instance.full_clean()

        assert len(instance.slug) < 200

    @given(django.from_model(
        CatalogCategory,
        weight=strategies.integers(
            max_value=-1,
            min_value=-2 ** 63,
        ),
    ))
    @settings(max_examples=10)
    def test_min_category_model_weight_properties(
        self, instance: CatalogCategory,
    ):
        """This test checks the validity of the weight category."""
        with pytest.raises(
            ValidationError,
            match='Ensure this value is greater than or equal to 0.',
        ):
            instance.full_clean()

        assert instance.weight <= 0
