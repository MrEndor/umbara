from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Homepage module config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.users'

    def ready(self) -> None:
        """Initialize module users."""
        from server.apps.users import signals  # noqa: F401, WPS433
