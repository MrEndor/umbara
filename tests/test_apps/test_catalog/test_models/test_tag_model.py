import pytest
from django.core.exceptions import ValidationError
from hypothesis import given, settings, strategies
from hypothesis.extra import django

from server.apps.catalog.models import CatalogTag


class TestTagModel(django.TestCase):
    """Class for testing tag model."""

    @given(django.from_model(
        CatalogTag,
        id=strategies.integers(
            min_value=1,
            max_value=(2 ** 63) - 1,
        ),
    ))
    @settings(max_examples=10)
    def test_tag_model_properties(self, instance: CatalogTag):
        """This test checks the general operability."""
        instance.save()

        assert instance.id > 0
        assert len(instance.name) <= 150
        assert isinstance(instance.is_published, bool)

    @given(django.from_model(
        CatalogTag,
        id=strategies.integers(
            max_value=0,
            min_value=-2 ** 63,
        ),
    ))
    @settings(max_examples=10)
    def test_raise_tag_model_id_properties(self, instance: CatalogTag):
        """This test checks the validity of the id tag."""
        with pytest.raises(
            ValidationError,
            match='Ensure this value is greater than or equal to 1.',
        ):
            instance.full_clean()

        assert instance.id <= 0

    @given(django.from_model(
        CatalogTag,
        id=strategies.integers(
            min_value=1,
            max_value=(2 ** 63) - 1,
        ),
        name=strategies.text(min_size=151),
    ))
    @settings(max_examples=10)
    def test_raise_tag_model_name_properties(self, instance: CatalogTag):
        """The test checks that the validity of the tag name."""
        with pytest.raises(
            ValidationError,
            match='Ensure this value has at most 150 characters',
        ):
            instance.full_clean()

        assert len(instance.name) > 150
