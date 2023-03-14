from http import HTTPStatus

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from server import settings
from server.apps.feedback import forms


@require_http_methods(request_method_list=['GET'])
def feedback(request: HttpRequest) -> HttpResponse:
    """View for feedback page."""
    feedback_from = forms.FeedbackForm()

    return render(
        request,
        'feedback/feedback.html',
        context={
            'form': feedback_from,
        },
    )


@require_http_methods(request_method_list=['POST'])
def create_feedback(request: HttpRequest) -> HttpResponse:
    """View for create feedback page."""
    feedback_form = forms.FeedbackForm(
        request.POST or None,
        request.FILES or None,
    )

    if not feedback_form.is_valid():
        return render(
            request,
            'feedback/feedback.html',
            context={
                'form': feedback_form,
            },
            status=HTTPStatus.BAD_REQUEST,
        )
    instance = feedback_form.save()
    feedback_form.save_m2m()

    messages.success(request, _('form_success'))

    send_mail(
        subject=request.user.get_username(),
        message=instance.text,
        from_email=settings.SERVER_EMAIL,  # type: ignore[attr-defined]
        fail_silently=False,
        recipient_list=[
            str(instance.personal_data.email),  # type: ignore[union-attr]
        ],
    )

    return redirect('feedback:feedback')
