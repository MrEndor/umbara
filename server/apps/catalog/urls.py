from django.urls import path

from server.apps.catalog.views import item_detail, item_list

app_name = 'catalog'

urlpatterns = [
    path('', item_list, name='item_list'),
    path('/<int:catalog_id>', item_detail, name='item_detail'),
]
