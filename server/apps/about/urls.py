from django.urls import path

from server.apps.about.views import description

app_name = 'about'

urlpatterns = [
    path('', description, name='description'),
]
