from django.urls.converters import register_converter


class OwnIntegerConverter:
    """Own number converter."""

    regex = '[0-9]+'

    def to_python(self, raw_number: str) -> int:
        """Converts a raw number to a python number."""
        return int(raw_number)

    def to_url(self, raw_number: str) -> str:
        """Does nothing."""
        return str(raw_number)


register_converter(OwnIntegerConverter, 'own_int')
