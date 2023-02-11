from typing import Final

from django.http import HttpRequest, HttpResponse

ITEM_LIST_TEXT: Final[str] = 'Список элементов'
ITEM_DETIAL_TEXT: Final[str] = 'Подробно элемент'


def item_list(request: HttpRequest) -> HttpResponse:
    """View for the item list."""
    return HttpResponse(
        '<body>{text}</body>'.format(text=ITEM_LIST_TEXT),
    )


def item_detail(request: HttpRequest, catalog_id: int) -> HttpResponse:
    """View for the item detail."""
    return HttpResponse(
        '<body>{text}</body>'.format(text=ITEM_DETIAL_TEXT),
    )
