from typing import List, Tuple

import pytest


@pytest.fixture(autouse=True)
def catalog_list_items_body() -> str:
    """Html fragment for list item page."""
    return '<body>Список элементов</body>'


@pytest.fixture(autouse=True)
def catalog_item_detail_body() -> str:
    """Html fragment for item detail page."""
    return '<body>Подробно элемент</body>'


@pytest.fixture(autouse=True)
def catalog_tag_normalized_names() -> List[Tuple[str, str]]:
    """Identical normalized names."""
    return [
        ('факtologiя', 'фактология'),
        ('adsqwe, asdasd', 'adsqweasdasd'),
        ('я простой текст', 'я!про*сто;й,текст'),
        ('hello world!', 'helloworld'),
        ('kak tak', 'как так'),
    ]


@pytest.fixture(autouse=True)
def catalog_tag_normalized_different_names() -> List[Tuple[str, str]]:
    """Different normalized names."""
    return [
        ('факtologiя', 'марктология'),
        ('adsqwe, asdasd', 'qwedfdas'),
        ('я простой текст', 'я?не!про*сто;й,текст'),
        ('hello world!', 'dlrowolleh'),
        ('kak tak', 'как не так'),
    ]
