# myapp/forms.py
from django import forms
from .models import DangerModel

class DangerForm(forms.ModelForm):
    class Meta:
        model = DangerModel
        fields = ['image',
                  'area']