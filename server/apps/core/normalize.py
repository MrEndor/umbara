from server.apps.core import constances


def normalize(string: str) -> str:
    """Normalize a string."""
    string = string.lower()
    table = string.maketrans(constances.REPLACEMENT_TABLE)

    return string.translate(table)
