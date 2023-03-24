from datetime import datetime

import jwt

from server import settings
from server.apps.users import models


def generate_jwt_token(
    user: models.UserWithProfile,
    before: datetime,
    after: datetime,
) -> str:
    """Create jwt token by user."""
    return jwt.encode(
        payload={
            'id': user.pk,
            'nbf': after,
            'exp': before,
        },
        key=settings.SECRET_KEY,  # type: ignore[attr-defined]
        algorithm=settings.JWT_ALGORITHM,  # type: ignore[attr-defined]
    )


def token_credentials(token) -> models.UserWithProfile:
    """Extract credentials from jwt."""
    payload = jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,  # type: ignore[attr-defined]
        algorithms=settings.JWT_ALGORITHM,  # type: ignore[attr-defined]
    )

    return models.UserWithProfile.objects.get(pk=payload['id'])
