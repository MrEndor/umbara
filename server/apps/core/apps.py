from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Catalog module config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.core'
