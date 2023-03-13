from typing import Union

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404


def pagination(
    object_list,
    page: Union[int, str],
    per_page=5,
):
    """Function to create a pagination page."""
    paginator = Paginator(object_list, per_page=per_page)

    try:
        return paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        raise Http404('No such page exists.')
