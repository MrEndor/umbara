from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def description(request: HttpRequest) -> HttpResponse:
    """View for project description."""
    return render(
        request,
        'about/index.html',
    )
