from django import forms
from .models import ChecklistEntry

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = ChecklistEntry
        fields = ['truefalse']