from typing import Final

from django.http import HttpRequest, HttpResponse

DESCRIPTION: Final[str] = 'О проекте'


def description(request: HttpRequest) -> HttpResponse:
    """View for project description."""
    return HttpResponse(
        '<body>{description}</body>'.format(description=DESCRIPTION),
    )
