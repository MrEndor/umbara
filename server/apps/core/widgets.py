from django.utils.safestring import mark_safe
from loguru import logger
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import current

TEMPLATE = """
<div style="float:left">
    <a style="width:{width}px;height:{height}px;
    display:block;margin:0 0 10px" class="thumbnail"
    target="_blank" href="{url}">
    <img src="{mini_url}"></a>{target}
</div>
"""


class AdminImageWidget(current.AdminImageWidget):
    """Widget for rendering thumbnails."""

    def render(
        self,
        name,
        value,
        attrs=None,
        **kwargs,
    ):  # pragma: no cover
        """Image rendering."""
        output = super().render(name, value, attrs, **kwargs)
        if not (value and hasattr(value, 'url')):  # noqa: WPS421
            return mark_safe(output)
        file_format = self._get_file_format(value)
        try:
            mini = get_thumbnail(
                value,
                self.attrs['thumb_size'],
                upscale=False,
                format=file_format,
            )
        except Exception:
            logger.exception('Unable to get the thumbnail')
        else:
            output = self._assemble_html(
                mini, value, output,
            )

        return mark_safe(output)

    def _assemble_html(self, mini, field, output) -> str:  # pragma: no cover
        try:
            output = TEMPLATE.format(
                width=mini.width,
                height=mini.height,
                url=field.url,
                mini_url=mini.url,
                target=output,
            )
        except (AttributeError, TypeError):
            logger.warning('Unable to get the thumbnail')
        return output

    def _get_file_format(self, field) -> str:  # pragma: no cover
        file_format = 'JPEG'
        aux_ext = str(field).split('.')

        try:
            aux_file_format = aux_ext[len(aux_ext) - 1].lower()  # noqa: WPS530
        except Exception:
            return file_format

        if aux_file_format in {'png', 'gif'}:
            file_format = aux_file_format.upper()

        return file_format
