from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from server.apps.core import fields
from server.apps.users import models


def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    """View for the user detail."""
    profile_prefetch = Prefetch(
        'profile',
        queryset=models.Profile.objects.only(
            fields.get_field_name(models.Profile.image),
            fields.get_field_name(models.Profile.coffee_count),
            fields.get_field_name(models.Profile.birthday),
            fields.get_field_name(models.Profile.user),
        ),
    )

    user = get_object_or_404(
        models.User.objects.filter(
            is_active=True,
        ).prefetch_related(
            profile_prefetch,
        ).only(
            fields.get_field_name(models.User.username),
            fields.get_field_name(models.User.email),
            fields.get_field_name(models.User.first_name),
            fields.get_field_name(models.User.last_name),
        ),
        username=username,
    )

    return render(
        request,
        'users/user_detail.html',
        context={
            'user': user,
        },
    )
