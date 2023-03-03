from django import forms

from server.apps.catalog.models import CatalogItem, ImageItem
from server.apps.core.widgets import AdminImageWidget


class CatalogItemAdminForm(forms.ModelForm[CatalogItem]):
    """CatalogItem photo display form."""

    class Meta:
        fields = '__all__'
        model = CatalogItem
        widgets = {
            'image': AdminImageWidget(
                attrs={'thumb_size': CatalogItem.thumb_size},
            ),
        }


class ImageItemAdminForm(forms.ModelForm[ImageItem]):
    """ImageItem photo display form."""

    class Meta:
        fields = '__all__'
        model = ImageItem
        widgets = {
            'image': AdminImageWidget(
                attrs={'thumb_size': ImageItem.thumb_size},
            ),
        }
