from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from hypothesis import given, settings

from server.apps.feedback.forms import FeedbackForm
from server.apps.feedback.models import Feedback, FeedbackPersonalData
from tests.strategies.feedback import base_feedback_form_strategy

FEEDBACK_FORM_KEY = 'form'


@pytest.mark.django_db()
def test_feedback_page(
    client: Client,
):
    """This test ensures that feedback page works."""
    response = client.get(reverse('feedback:feedback'))

    assert FEEDBACK_FORM_KEY in response.context
    form: FeedbackForm = response.context[FEEDBACK_FORM_KEY]

    email_field = form.fields['email']
    text_field = form.fields['text']

    assert email_field.help_text == 'example@example.com'
    assert email_field.label == _('Your email')
    assert text_field.label == _('Your message')


@pytest.mark.django_db()
@given(
    form=base_feedback_form_strategy,
)
@settings(max_examples=10)
def test_feedback_create_page(  # noqa: WPS210, WPS218
    client: Client,
    form: FeedbackForm,
):
    """This test ensures that feedback page works."""
    fields = form.data
    response = client.post(
        reverse('feedback:create'), data=fields,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == reverse('feedback:feedback')

    personal_data = FeedbackPersonalData.objects.filter(
        email=fields['email'],
    )

    assert personal_data.exists()

    feedback = Feedback.objects.filter(
        personal_data=personal_data.get(),
        text=fields['text'],
    )

    files = feedback.last().files  # type: ignore[union-attr]

    assert files.exists()  # type: ignore[union-attr]

    for uploaded_file in files.all():  # type: ignore[union-attr]
        response = client.get(uploaded_file.file.url)

        assert response.status_code == HTTPStatus.OK

    feedback.delete()


@pytest.mark.django_db(transaction=True)
def test_error_feedback_create_page(client: Client):
    """This test ensures that feedback create page raise 400."""
    response = client.post(
        reverse('feedback:create'),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
