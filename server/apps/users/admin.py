from django.contrib import admin
from django.contrib.auth import models as admin_models
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from server.apps.users import models

admin.site.unregister(admin_models.User)


class ProfileUserInline(
    admin.TabularInline[models.Profile, admin_models.User],
):
    """ProfileUser inline admin."""

    model = models.Profile
    can_delete = False


@admin.register(models.UserWithProfile)
class UserAdmin(AuthUserAdmin):
    """User admin."""

    inlines = (ProfileUserInline,)
