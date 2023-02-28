from django.urls import path, re_path

from server.apps.catalog.views import item_detail, item_list

app_name = 'catalog'

urlpatterns = [
    path('', item_list, name='item_list'),
    path('<int:product_id>', item_detail, name='item_detail'),
    re_path('^re/(?P<product_id>[0-9]+)/$', item_detail, name='re_item_detail'),
    path(
        'converter/<own_int:product_id>',
        item_detail,
        name='convert_item_detail',
    ),
]
