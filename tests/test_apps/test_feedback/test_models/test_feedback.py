from hypothesis import given, settings
from hypothesis.extra import django

from server.apps.feedback.models import Feedback


class TestCategoryModel(django.TestCase):
    """Class for testing category model."""

    @given(django.from_model(
        Feedback,
    ))
    @settings(max_examples=10)
    def test_feedback_model_properties(
        self, instance: Feedback,
    ):
        """This test checks the general operability."""
        instance.save()

        assert instance.id > 0
        assert len(instance.text) <= 255
        assert len(str(instance))
        assert len(str(instance.personal_data))
