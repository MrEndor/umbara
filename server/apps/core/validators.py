from functools import wraps
from typing import Callable

from django.core.exceptions import ValidationError


def is_contains(*words) -> Callable[[str], None]:
    """Validator for checking words in text."""
    if not words:
        raise ValueError('Words must not be empty')

    @wraps(is_contains)
    def validator(text: str):  # noqa: WPS430
        tokens = text.lower().split()
        contains = [
            word.lower() in tokens for word in words
        ]
        if any(contains):
            return

        raise ValidationError(
            'Текст должен содержать одно из слов: {words}'.format(
                words=', '.join(words),
            ),
        )

    return validator
