import pytest
from django.core.exceptions import ValidationError
from hypothesis import given, strategies

from server.apps.core.validators import ContainsValidator


@given(
    text=strategies.text(),
)
def test_not_contain(text: str):
    """This test verifies that there are no words in the line."""
    validator = ContainsValidator(
        'not contain',
    )  # type: ignore[no-untyped-call]

    with pytest.raises(
        ValidationError,
        match='Текст должен содержать одно из слов',
    ):
        validator(text)


@given(
    text=strategies.from_regex('[a-zA-Z]', fullmatch=True),
    word=strategies.from_regex('[a-zA-Z]', fullmatch=True),
)
def test_is_contain(text: str, word: str):
    """This test verifies that the word is in the string."""
    validator = ContainsValidator(word)  # type: ignore[no-untyped-call]

    validator(' '.join([text, word]))


def test_empty_words_is_contain():
    """This test verifies that blank words are handled correctly."""
    with pytest.raises(
        ValueError,
        match='Words must not be empty',
    ):
        ContainsValidator()  # type: ignore[no-untyped-call]
