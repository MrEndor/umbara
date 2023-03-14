from django.core.files.uploadedfile import SimpleUploadedFile
from hypothesis import strategies
from hypothesis.extra import django

from server.apps.feedback import forms


@strategies.composite
def files(
    draw,
):
    """Function to add images."""
    return SimpleUploadedFile(
        'cat.txt',
        content=draw(strategies.binary(min_size=100)),
        content_type='text/plain',
    )


base_feedback_form_strategy = django.from_form(
    forms.FeedbackForm,  # type: ignore[arg-type]
    feedback_files=strategies.lists(files(), min_size=1, max_size=10),
)
