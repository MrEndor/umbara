from datetime import datetime, timedelta, timezone

from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.core.mail import send_mail
from django.template.loader import render_to_string

from server import settings
from server.apps.users import constants, jwt, models


def create_user(  # noqa: WPS210
    form: UserCreationForm[models.UserWithProfile],
    site: Site | RequestSite,
):
    """Function for create user with activate email."""
    form.instance.is_active = (
        settings.INITIAL_ACTIVATION  # type: ignore[attr-defined]
    )
    user = form.save()

    if settings.INITIAL_ACTIVATION:  # type: ignore[attr-defined]
        return

    now = datetime.now(tz=timezone.utc)

    works_before = now + timedelta(
        days=constants.DAYS_TOKEN_ACTIVE,
        hours=constants.AFTER_HOURS_ACTIVATE_TOKEN,
    )
    activate_after = now + timedelta(
        hours=constants.AFTER_HOURS_ACTIVATE_TOKEN,
    )

    token = jwt.generate_jwt_token(
        user,
        before=works_before,
        after=activate_after,
    )

    message = render_to_string(
        template_name='users/email/activation.html',
        context={
            'token': token,
            'domain': site.domain,
            'site_name': site.name,
            'protocol': 'http',
            'user': user,
        },
    )

    send_mail(
        subject=user.get_username(),
        message=message,
        from_email=settings.SERVER_EMAIL,  # type: ignore[attr-defined]
        fail_silently=False,
        recipient_list=[
            str(user.email),
        ],
    )
