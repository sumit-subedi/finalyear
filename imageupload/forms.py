from django import forms
from .models import image


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = image
        fields ='__all__'