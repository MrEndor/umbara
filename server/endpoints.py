from http import HTTPStatus
from typing import Final

from django.http import HttpRequest, HttpResponse

COFFEE_TEXT: Final[str] = 'Я чайник'


def coffee(request: HttpRequest) -> HttpResponse:
    """Im a teapot."""
    if request.user.is_authenticated:
        profile = request.user.profile
        profile.coffee_count += 1
        profile.save()

    return HttpResponse(
        '<body>{text}</body>'.format(text=COFFEE_TEXT),
        status=HTTPStatus.IM_A_TEAPOT,
    )
