import pytest


@pytest.fixture(autouse=True)
def homepage_body() -> str:
    """Html fragment for home page."""
    return '<body>Главная</body>'
