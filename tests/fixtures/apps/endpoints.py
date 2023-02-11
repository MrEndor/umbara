import pytest


@pytest.fixture(autouse=True)
def coffee_body() -> str:
    """Html fragment for coffee page."""
    return '<body>Я чайник</body>'
