from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from hypothesis import given, settings
from hypothesis.extra import django

from server.apps.feedback.forms import FeedbackForm
from server.apps.feedback.models import Feedback

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
    form=django.from_form(
        FeedbackForm,  # type: ignore[arg-type]
    ),
)
@settings(max_examples=10)
def test_feedback_create_page(
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

    assert Feedback.objects.filter(
        email=fields['email'],
        text=fields['text'],
    ).exists()


@pytest.mark.django_db(transaction=True)
def test_error_feedback_create_page(client: Client):
    """This test ensures that feedback create page raise 400."""
    response = client.post(
        reverse('feedback:create'),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
