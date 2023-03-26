from datetime import datetime, timedelta, timezone

from axes import signals
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string

from server import settings
from server.apps.users import constants, jwt, models


@receiver(signals.user_locked_out)
def send_email_to_unlock(  # noqa: WPS210
    sender: str, *args, **kwargs,
):
    """Signal to send an account unlock email."""
    user_query = models.UserWithProfile.objects.filter(
        username=kwargs['username'],
    )

    if not user_query.exists():
        return
    user = user_query.get()
    site = get_current_site(kwargs['request'])
    now = datetime.now(tz=timezone.utc)

    token = jwt.generate_jwt_token(
        user,
        after=now,
        before=now + timedelta(
            weeks=constants.WEEKS_TOKEN_UNLOCK_USER_WORKS,
        ),
    )

    message = render_to_string(
        template_name='users/email/unlock.html',
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
