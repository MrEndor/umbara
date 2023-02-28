from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """View for project homepage."""
    return render(
        request, 'homepage/index.html',
    )
