from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ContainsValidator:
    """Validator for checking words in text."""

    def __init__(self, *words):
        """Words that should be in the text."""
        self.words = words
        self._validate_words()

    def __call__(self, text: str) -> None:
        """Validate func."""
        tokens = text.lower()
        contains = [
            word.lower() in tokens for word in self.words
        ]
        if any(contains):
            return

        raise ValidationError(
            'Текст должен содержать одно из слов: {words}'.format(
                words=', '.join(self.words),
            ),
        )

    def _validate_words(self) -> None:
        if self.words:
            return
        raise ValueError('Words must not be empty')
