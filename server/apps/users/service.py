from datetime import datetime, timedelta

import jwt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.core.mail import send_mail
from django.template.loader import render_to_string

from server import settings
from server.apps.users import constants, models


def _generate_jwt_token(user: models.User) -> str:
    """Create jwt token by user."""
    now = datetime.now()

    time = now + timedelta(
        days=constants.DAYS_TOKEN_ACTIVE,
        hours=constants.AFTER_HOURS_ACTIVATE_TOKEN,
    )
    activate_after = now + timedelta(
        hours=constants.AFTER_HOURS_ACTIVATE_TOKEN,
    )

    return jwt.encode(
        payload={
            'id': user.pk,
            'exp': time,
            'nbf': activate_after,
        },
        key=settings.SECRET_KEY,  # type: ignore[attr-defined]
        algorithm=settings.JWT_ALGORITHM,  # type: ignore[attr-defined]
    )


def token_credentials(token) -> models.User:
    """Extract credentials from jwt."""
    payload = jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,  # type: ignore[attr-defined]
        algorithms=settings.JWT_ALGORITHM,  # type: ignore[attr-defined]
    )

    return models.User.objects.get(pk=payload['id'])


def create_user(
    form: UserCreationForm[models.User],
    site: Site | RequestSite,
):
    """Function for create user with activate email."""
    form.instance.is_active = (
        settings.INITIAL_ACTIVATION  # type: ignore[attr-defined]
    )
    user = form.save()
    models.Profile.objects.create(user=user)  # type: ignore[misc]

    if settings.INITIAL_ACTIVATION:  # type: ignore[attr-defined]
        return

    token = _generate_jwt_token(user)

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
