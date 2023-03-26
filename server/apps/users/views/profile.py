from http import HTTPStatus
from typing import cast

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from server.apps.users import forms, models


@login_required
@require_http_methods(request_method_list=['GET'])
def profile(request: HttpRequest) -> HttpResponse:
    """View for the profile."""
    user = cast(models.UserWithProfile, request.user)
    user_form = forms.UserForm(
        instance=user,
    )
    profile_form = forms.ProfileForm(
        instance=user.profile,
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
    user = cast(models.UserWithProfile, request.user)
    user_form = forms.UserForm(
        request.POST or None,
        instance=user,
    )
    profile_form = forms.ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=user.profile,
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

    return render(
        request,
        'users/profile.html',
        context={
            'user_form': user_form,
            'profile_form': profile_form,
        },
    )
