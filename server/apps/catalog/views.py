from datetime import date, timedelta

from django.db.models import F  # noqa: WPS347
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from server.apps.catalog.constants import FRIDAY, PRODUCT_PAGE
from server.apps.catalog.models import CatalogItem
from server.apps.core.pagination import pagination


def extract_page(request, default: int):
    """Extract page number from request."""
    return request.GET.get('page', default=default)


def item_list(request: HttpRequest) -> HttpResponse:
    """View for the item list."""
    products = CatalogItem.objects.list_products()
    page_number = extract_page(request, 1)

    page_obj = pagination(products, page_number)

    return render(
        request,
        'catalog/products.html',
        context={PRODUCT_PAGE: page_obj},
    )


def item_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    """View for the item detail."""
    product = CatalogItem.objects.get_detail_by(pk=product_id)

    if not product:
        raise Http404('No such page exists.')

    return render(
        request,
        'catalog/details.html',
        context={'product': product},
    )


def new_products_list(request: HttpRequest) -> HttpResponse:
    """View for the new product list."""
    today = date.today()

    products = CatalogItem.objects.list_random_products(
        updated_at__gte=today - timedelta(days=7),
    ).reverse()[:5]

    return render(
        request,
        'catalog/sections.html',
        context={
            PRODUCT_PAGE: products,
            'section': _('New Products'),
        },
    )


def friday_products_list(request: HttpRequest) -> HttpResponse:
    """View for the friday product list."""
    products = CatalogItem.objects.list_products(
        updated_at__week_day=FRIDAY,
    ).order_by('-updated_at')

    return render(
        request,
        'catalog/sections.html',
        context={
            PRODUCT_PAGE: products[:5],
            'section': _('Friday Products'),
        },
    )


def old_products_list(request: HttpRequest) -> HttpResponse:
    """View for the old product list."""
    products = CatalogItem.objects.list_products(
        updated_at=F('created_at'),
    )
    page_number = extract_page(request, 1)

    page_obj = pagination(products, page_number)

    return render(
        request,
        'catalog/sections.html',
        context={
            PRODUCT_PAGE: page_obj,
            'section': _('Old Products'),
        },
    )
