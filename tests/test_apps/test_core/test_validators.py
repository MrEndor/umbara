import pytest
from django.core.exceptions import ValidationError
from hypothesis import given, strategies

from server.apps.core.validators import is_contains


@given(
    text=strategies.text(),
)
def test_not_contain(text: str):
    """This test verifies that there are no words in the line."""
    func = is_contains('not contain')

    with pytest.raises(
        ValidationError,
        match='Текст должен содержать одно из слов',
    ):
        func(text)


@given(
    text=strategies.from_regex('[a-zA-Z]', fullmatch=True),
    word=strategies.from_regex('[a-zA-Z]', fullmatch=True),
)
def test_is_contain(text: str, word: str):
    """This test verifies that the word is in the string."""
    func = is_contains(word)

    func(' '.join([text, word]))


def test_empty_words_is_contain():
    """This test verifies that blank words are handled correctly."""
    with pytest.raises(
        ValueError,
        match='Words must not be empty',
    ):
        is_contains()
