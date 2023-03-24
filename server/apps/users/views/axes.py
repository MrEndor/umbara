from axes.utils import reset
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from jwt import exceptions

from server.apps.users import jwt


def unlock(request: HttpRequest, token: str):
    """View for unlock account."""
    try:
        user = jwt.token_credentials(token)
    except exceptions.InvalidTokenError:
        messages.error(request, _('Token is invalid'))
        return redirect('users:login')

    reset(username=user.username)
    messages.success(request, _('Account successfully unlocked'))

    return redirect('users:login')
