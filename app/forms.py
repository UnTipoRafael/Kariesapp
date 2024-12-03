from django import forms
from .models import ImagenLocal, ImagenDrive

class ImagenLocalForm(forms.ModelForm):
    class Meta:
        model = ImagenLocal
        fields = ['name', 'imagen']

class ImagenDriveForm(forms.ModelForm):
    class Meta:
        model = ImagenDrive
        fields = ['name', 'imagen']