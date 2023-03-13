from http import HTTPStatus

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from server import settings
from server.apps.feedback.forms import FeedbackForm


@require_http_methods(request_method_list=['GET'])
def feedback(request: HttpRequest) -> HttpResponse:
    """View for feedback page."""
    form = FeedbackForm()

    return render(
        request,
        'feedback/feedback.html',
        context={
            'form': form,
        },
    )


@require_http_methods(request_method_list=['POST'])
def create_feedback(request: HttpRequest) -> HttpResponse:
    """View for create feedback page."""
    form = FeedbackForm(request.POST or None)

    if not form.is_valid():
        return render(
            request,
            'feedback/feedback.html',
            context={
                'form': form,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    model = form.save()
    messages.success(request, _('form_success'))

    send_mail(
        subject=request.user.get_username(),
        message=model.text,
        from_email=settings.SERVER_EMAIL,  # type: ignore[attr-defined]
        fail_silently=False,
        recipient_list=[model.email],
    )

    return redirect('feedback:feedback')
