from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from server.apps.users import models


def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    """View for the user detail."""
    user = models.UserWithProfile.objects.get_user_detail(
        username=username,
    )

    if not user:
        raise Http404('No such page exists.')

    return render(
        request,
        'users/user_detail.html',
        context={
            'user': user,
        },
    )
