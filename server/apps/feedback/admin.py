from django.contrib import admin

from server.apps.feedback import models

admin.site.register(models.Feedback)
