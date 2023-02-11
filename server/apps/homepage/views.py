from typing import Final

from django.http import HttpRequest, HttpResponse

HOMEPAGE_TEXT: Final[str] = 'Главная'


def home(request: HttpRequest) -> HttpResponse:
    """View for project homepage."""
    return HttpResponse(
        '<body>{homepage}</body>'.format(homepage=HOMEPAGE_TEXT),
    )
