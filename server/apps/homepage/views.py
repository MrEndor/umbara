from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from server.apps.catalog.logic.queries import item


def home(request: HttpRequest) -> HttpResponse:
    """View for project homepage."""
    products = item.all_on_main()

    page_number = request.GET.get('page', default=1)

    paginator = Paginator(products, per_page=5)

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        raise Http404('No such page exists.')

    context = {
        'product_page': page_obj,
    }

    return render(
        request, 'homepage/index.html', context,
    )
