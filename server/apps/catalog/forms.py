from ckeditor import fields
from ckeditor.widgets import CKEditorWidget
from django import forms

from server.apps.catalog.models import CatalogItem


class CatalogItemAdminForm(forms.ModelForm[CatalogItem]):
    """Form for editing a description."""

    text = fields.RichTextFormField(widget=CKEditorWidget())

    class Meta:
        model = CatalogItem
        fields = '__all__'
