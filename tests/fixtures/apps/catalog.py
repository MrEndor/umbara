from typing import List, Tuple

import pytest


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


@pytest.fixture(autouse=True, scope='class')
def item_list_not_deferred_fields():
    """Fixture for deferred item list fields."""
    return {
        'catalog',
        'name',
        'image',
        'tags',
        'text',
    }


@pytest.fixture(autouse=True)
def item_detail_not_deferred_fields():
    """Fixture for deferred item detail fields."""
    return {
        'catalog',
        'name',
        'image',
        'gallery',
        'tags',
        'text',
    }
