from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from server.apps.core.pagination import pagination
from server.apps.users import models


def user_list(request: HttpRequest) -> HttpResponse:
    """View for the list users."""
    users = models.UserWithProfile.objects.list_active_users()

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
