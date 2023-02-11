import pytest


@pytest.fixture(autouse=True)
def description_body() -> str:
    """Html fragment for description page."""
    return '<body>О проекте</body>'
