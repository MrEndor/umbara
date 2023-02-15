from django.urls import path

from server.apps.homepage.views import home

app_name = 'homepage'

urlpatterns = [
    path('', home, name='home'),
]
