from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, label='아이디', widget=forms.TextInput(attrs={"placeholder": "사용자명(3자리 이상)"},),)
    password = forms.CharField(min_length=4, label='비밀번호', widget=forms.PasswordInput(attrs={"placeholder": "비밀번호(4자리 이상)"},),)