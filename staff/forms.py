from django import forms
from .models import LandDocument

class LandDocumentForm(forms.ModelForm):
    class Meta:
        model = LandDocument
        fields = ['title', 'description', 'file']