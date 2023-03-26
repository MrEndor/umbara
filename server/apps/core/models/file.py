from pathlib import Path
from typing import TypeVar
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

FileModel = TypeVar('FileModel', bound='FileMixin')


def get_upload_to(instance: FileModel, filename: str):
    """Function for set upload_to."""
    return instance.get_path(filename)


class FileMixin(models.Model):
    """Mixin for model files."""

    file = models.FileField(
        verbose_name=_('uploaded file'),
        upload_to=get_upload_to,
    )

    class Meta:
        abstract = True

    def get_path(self, filename: str) -> str:
        """Function for get file path."""
        file_format = Path(filename).suffix
        return '{id}{format}'.format(
            id=uuid4(),
            format=file_format,
        )
