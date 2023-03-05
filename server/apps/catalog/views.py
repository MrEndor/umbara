from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from server.apps.catalog.logic.queries import item


def item_list(request: HttpRequest) -> HttpResponse:
    """View for the item list."""
    products = item.list_products()
    page_number = request.GET.get('page', default=1)

    paginator = Paginator(products, per_page=5)

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        raise Http404('No such page exists.')

    return render(
        request,
        'catalog/products.html',
        context={'product_page': page_obj},
    )


def item_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    """View for the item detail."""
    product = item.get_detail_by(pk=product_id)

    if not product:
        raise Http404('No such page exists.')

    return render(
        request,
        'catalog/details.html',
        context={'product': product},
    )
