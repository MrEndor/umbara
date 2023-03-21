"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import hypothesis
import pytest

pytest_plugins = [
    'tests.fixtures.apps.catalog',
    'tests.fixtures.apps.endpoints',
]

hypothesis.settings.register_profile(
    'test', parent=hypothesis.settings(
        suppress_health_check=[
            hypothesis.HealthCheck.function_scoped_fixture,
            hypothesis.HealthCheck.too_slow,
            hypothesis.HealthCheck.filter_too_much,
        ],
        max_examples=500,
        deadline=1500,
        stateful_step_count=150,
    ),
)


@pytest.fixture(autouse=True)
def _password_hashers(settings) -> None:
    """Forces django to use fast password hashers for tests."""
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture(autouse=True)
def _auth_backends(settings) -> None:
    """Deactivates security backend from Axes app."""
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )


@pytest.fixture(autouse=True)
def _debug(settings) -> None:
    """Sets proper DEBUG and TEMPLATE debug mode for coverage."""
    settings.DEBUG = False
    for template in settings.TEMPLATES:
        template['OPTIONS']['debug'] = True


@pytest.fixture(autouse=True)
def _email_backend(settings):
    """Forces django to use locmem email backend."""
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
