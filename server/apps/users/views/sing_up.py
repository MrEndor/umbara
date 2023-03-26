from http import HTTPStatus

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from jwt import exceptions

from server.apps.users import forms, jwt, service


@require_http_methods(request_method_list=['GET'])
def signup(request: HttpRequest) -> HttpResponse:
    """View for the signup."""
    form = forms.UserCreationForm()

    return render(
        request,
        'users/auth/signup.html',
        context={
            'form': form,
        },
    )


@require_http_methods(request_method_list=['POST'])
def create_signup(request: HttpRequest) -> HttpResponse:
    """View for the create signup."""
    form = forms.UserCreationForm(request.POST or None)

    if not form.is_valid():
        return render(
            request,
            'users/auth/signup.html',
            context={
                'form': form,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    service.create_user(
        form,
        get_current_site(request),
    )

    return redirect('users:login')


@require_http_methods(request_method_list=['GET'])
def activate_user(request: HttpRequest, token: str):
    """View for the active user page."""
    try:
        user = jwt.token_credentials(token)
    except exceptions.ImmatureSignatureError:
        messages.error(request, _('Token not activated yet'))
        return redirect('users:login')
    except exceptions.InvalidTokenError:
        messages.error(request, _('Token is invalid'))
        return redirect('users:login')

    user.is_active = True
    user.save()
    messages.success(request, _('Account successfully activated'))

    return redirect('users:activate_done')
