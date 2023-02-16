from http import HTTPStatus
from typing import Final

from django.http import HttpRequest, HttpResponse

COFFEE_TEXT: Final[str] = 'Я чайник'


def coffee(request: HttpRequest) -> HttpResponse:
    """Im a teapot."""
    return HttpResponse(
        '<body>{text}</body>'.format(text=COFFEE_TEXT),
        status=HTTPStatus.IM_A_TEAPOT,
    )
