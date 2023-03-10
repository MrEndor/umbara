import re

from server.apps.core import constants


def add_header_middleware(get_response):  # pragma: no cover
    """Middleware for add http header Content-Disposition."""
    regex = re.compile(constants.IMAGES_REGEX)

    def middleware(request):  # noqa: WPS430
        response = get_response(request)
        if not regex.fullmatch(request.get_full_path()):
            return response

        response['Content-Disposition'] = 'attachment'

        return response
    return middleware
