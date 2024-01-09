from django import forms
from .models import ChecklistEntry

class ChecklistForm(forms.Form):
    item_1 = forms.BooleanField()
    item_2 = forms.BooleanField()
    item_3 = forms.BooleanField()
    item_4 = forms.BooleanField()
    item_5 = forms.BooleanField()
    item_6 = forms.BooleanField()
    item_7 = forms.BooleanField()
    item_8 = forms.BooleanField()
    item_9 = forms.BooleanField()
    item_10 = forms.BooleanField()
    item_11 = forms.BooleanField()
    item_12 = forms.BooleanField()