from typing import Dict, Final

MAX_NAME_LENGTH: Final[int] = 150
MAX_SLUG_LENGTH: Final[int] = 200
REGEX_SLUG: Final[str] = '^[0-9-_a-zA-Z]+$'
MIN_ID: Final[int] = 1

_symbols = [  # noqa: WPS317
    '?', ' ', ',', '.', '!', '"', ';', ':', '(', ')',
    '^', '<', '>', '@', '$', '№', '%', '*',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
]
REPLACEMENT_TABLE: Final[Dict[str, str]] = {  # noqa: WPS317
    'a': 'а', 'e': 'е', 'y': 'у',
    'v': 'в', 'c': 'с', 'p': 'р',
    'o': 'о', 'k': 'к', 'n': 'н',
    'g': 'г', 't': 'т', 'l': 'л', 'i': 'и',
} | {symbol: '' for symbol in _symbols}

DEFAULT_GEOMETRY_STRING = '300x300'
