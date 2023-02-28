from typing import Final

from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from server.apps.catalog.models import CatalogItem

ITEM_LIST_TEXT: Final[str] = 'Список элементов'
ITEM_DETIAL_TEXT: Final[str] = 'Подробно элемент'


def item_list(request: HttpRequest) -> HttpResponse:
    """View for the item list."""
    products = CatalogItem.objects.exclude(
        is_published=False,
    ).all()
    page_number = request.GET.get('page', default=1)

    paginator = Paginator(products, per_page=5)
    page_obj = paginator.page(page_number)

    return render(
        request,
        'catalog/products.html',
        context={'product_page': page_obj},
    )


def item_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    """View for the item detail."""
    product = CatalogItem.objects.get(
        id=product_id,
    )

    return render(
        request,
        'catalog/details.html',
        context={'product': product},
    )
