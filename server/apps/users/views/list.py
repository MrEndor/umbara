from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from server.apps.core import fields
from server.apps.core.pagination import pagination
from server.apps.users import models


def user_list(request: HttpRequest) -> HttpResponse:
    """View for the list users."""
    profile_prefetch = Prefetch(
        'profile',
        queryset=models.Profile.objects.only(
            fields.get_field_name(models.Profile.image),
            fields.get_field_name(models.Profile.user),
        ),
    )

    users = models.User.objects.filter(
        is_active=True,
    ).prefetch_related(
        profile_prefetch,
    ).only(
        fields.get_field_name(models.User.username),
    )

    page = request.GET.get('page', default=1)

    paginator = pagination(
        users, page,
    )

    return render(
        request,
        'users/user_list.html',
        context={
            'users_page': paginator,
        },
    )
