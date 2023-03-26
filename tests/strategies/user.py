from hypothesis import strategies
from hypothesis.extra import django

from server.apps.users import forms

base_user_signup_form_strategy = django.from_form(
    forms.UserCreationForm,  # type: ignore[arg-type]
    username=strategies.text(
        alphabet=strategies.from_regex(
            '^[a-zA-Z]$', fullmatch=True,
        ),
        min_size=10,
        max_size=50,
    ),
    password1=strategies.just('test'),
    password2=strategies.just('test'),
)
