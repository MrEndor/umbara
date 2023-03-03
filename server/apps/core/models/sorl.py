from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField, get_thumbnail

from server.apps.core.constants import DEFAULT_GEOMETRY_STRING

TEMPLATE = """
<div style="float:left">
    <a style="width:{width}px;height:{height}px;
    display:block;margin:0 0 10px" class="thumbnail"
    target="_blank" href="{url}">
    <img src="{mini_url}"></a>
</div>'
"""


class ImageMixin(models.Model):
    """Mixin for sorl image."""

    image = ImageField(
        upload_to='images',
        verbose_name=_('image'),
        null=True,
    )

    thumb_size = DEFAULT_GEOMETRY_STRING

    class Meta:
        verbose_name = 'ImageMixin'
        abstract = True

    def view_image(self):  # pragma: no cover
        """View of sorl image."""
        image = self.image

        mini = get_thumbnail(
            image,
            self.thumb_size,
            upscale=False,
        )
        output = TEMPLATE.format(
            width=mini.width,
            height=mini.height,
            url=image.url,
            mini_url=mini.url,
        )
        return mark_safe(output)  # noqa: S308, S703
