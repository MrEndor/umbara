from django.urls import path

from server.apps.feedback.views import create_feedback, feedback

app_name = 'feedback'

urlpatterns = [
    path('', feedback, name='feedback'),
    path('create', create_feedback, name='create'),
]
