from django.urls import path, re_path

from server.apps.catalog.views import (
    friday_products_list,
    item_detail,
    item_list,
    new_products_list,
    old_products_list,
)

app_name = 'catalog'

urlpatterns = [
    path('', item_list, name='item_list'),
    path('<int:product_id>', item_detail, name='item_detail'),
    path('section/new', new_products_list, name='item_new_products'),
    path('section/friday', friday_products_list, name='item_friday_products'),
    path('section/old', old_products_list, name='item_old_products'),
    re_path('^re/(?P<product_id>[0-9]+)/$', item_detail, name='re_item_detail'),
    path(
        'converter/<own_int:product_id>',
        item_detail,
        name='convert_item_detail',
    ),
]
