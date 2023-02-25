from server.apps.core import constants


def normalize(string: str) -> str:
    """Normalize a string."""
    string = string.lower()
    table = string.maketrans(constants.REPLACEMENT_TABLE)

    return string.translate(table)
