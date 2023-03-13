from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from server.apps.catalog.models import CatalogItem
from server.apps.core.pagination import pagination


def home(request: HttpRequest) -> HttpResponse:
    """View for project homepage."""
    products = CatalogItem.objects.list_products(is_on_main=True)

    page_number = request.GET.get('page', default=1)

    page_obj = pagination(products, page_number)

    context = {
        'product_page': page_obj,
    }

    return render(
        request, 'homepage/index.html', context,
    )
