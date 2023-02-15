import pytest


@pytest.fixture(autouse=True)
def catalog_list_items_body() -> str:
    """Html fragment for list item page."""
    return '<body>Список элементов</body>'


@pytest.fixture(autouse=True)
def catalog_item_detail_body() -> str:
    """Html fragment for item detail page."""
    return '<body>Подробно элемент</body>'
