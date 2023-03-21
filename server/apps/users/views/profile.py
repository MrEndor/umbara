from http import HTTPStatus
from typing import cast

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from server.apps.users import forms


@login_required
@require_http_methods(request_method_list=['GET'])
def profile(request: HttpRequest) -> HttpResponse:
    """View for the profile."""
    user_form = forms.UserForm(
        instance=cast(User, request.user),
    )
    profile_form = forms.ProfileForm(
        instance=cast(User, request.user).profile,
    )

    return render(
        request,
        'users/profile.html',
        context={
            'user_form': user_form,
            'profile_form': profile_form,
        },
    )


@login_required
@require_http_methods(request_method_list=['POST'])
def change_profile(request: HttpRequest) -> HttpResponse:
    """View for the change profile."""
    user_form = forms.UserForm(
        request.POST or None,
        instance=cast(User, request.user),
    )
    profile_form = forms.ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=cast(User, request.user).profile,
    )

    request_forms = (
        user_form.is_valid(),
        profile_form.is_valid(),
    )

    if not all(request_forms):
        return render(
            request,
            'users/profile.html',
            context={
                'user_form': user_form,
                'profile_form': profile_form,
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    user_form.save()
    profile_form.save()

    return render(
        request,
        'users/profile.html',
        context={
            'user_form': user_form,
            'profile_form': profile_form,
        },
    )
