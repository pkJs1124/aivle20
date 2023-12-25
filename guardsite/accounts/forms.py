from django import forms
from django.core.exceptions import ValidationError
from accounts.models import User

# 로그인
class LoginForm(forms.Form):
    username = forms.CharField(min_length=1, label='아이디', widget=forms.TextInput(),)
    password = forms.CharField(min_length=1, label='비밀번호', widget=forms.PasswordInput(),)
    role = forms.ChoiceField(choices=User.ROLES, widget=forms.RadioSelect())
    
# 회원가입
class SignupForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    person_name = forms.CharField(label='이름')
    phone_number = forms.CharField(label='전화번호')
    company = forms.CharField(label='회사', widget=forms.TextInput(),)
    role = forms.ChoiceField(choices=User.ROLES, widget=forms.RadioSelect)
    
    # 아이디 유효성 검사
    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"입력한 아이디({username})는 이미 사용 중입니다.")
        return username
    
    # 비밀번호 유효성 검사
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        
        # 비밀번호 길이가 8자 이상인지 확인
        if len(password1) < 8:
            raise forms.ValidationError("비밀번호는 최소 8자리 이상이어야 합니다.")

        # 대소문자, 특수문자, 숫자 중 최소 2종류 이상을 포함하는지 확인
        char_types = 0
        if any(char.isupper() for char in password1):
            char_types += 1
        if any(char.islower() for char in password1):
            char_types += 1
        if any(char.isdigit() for char in password1):
            char_types += 1
        if any(char.isascii() and not char.isalnum() for char in password1):
            char_types += 1

        if char_types < 3:
            raise forms.ValidationError("비밀번호는 대소문자, 특수문자, 숫자 중 최소 3종류 이상을 포함해야 합니다.")
        return password1
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password1 != password2:
            raise forms.ValidationError("두 비밀번호가 일치하지 않습니다.")
        return password2

    # 전화번호 유효성 검사
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        
        if phone_number and not phone_number.isdigit():
            raise ValidationError("전화번호는 숫자만 포함해야 합니다.")
        
        if len(phone_number) != 11:
            raise ValidationError("전화번호는 11자리여야 합니다.")
        
        return phone_number
    
# 아이디 찾기
class FindForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['person_name', 'phone_number']
        
# 비밀번호 찾기
class FindpasswordForm(forms.Form):
    username = forms.CharField()
    phone_number = forms.CharField(label='전화번호')
        
# 비밀번호 재설정
class ResetPasswordForm(forms.Form):       
    new_password1 = forms.CharField(label='새 비밀번호', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    
    # 비밀번호 유효성 검사
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        
        # 비밀번호 길이가 8자 이상인지 확인
        if len(new_password1) < 8:
            raise forms.ValidationError("비밀번호는 최소 8자리 이상이어야 합니다.")

        # 대소문자, 특수문자, 숫자 중 최소 2종류 이상을 포함하는지 확인
        char_types = 0
        if any(char.isupper() for char in new_password1):
            char_types += 1
        if any(char.islower() for char in new_password1):
            char_types += 1
        if any(char.isdigit() for char in new_password1):
            char_types += 1
        if any(char.isascii() and not char.isalnum() for char in new_password1):
            char_types += 1

        if char_types < 3:
            raise forms.ValidationError("비밀번호는 대소문자, 특수문자, 숫자 중 최소 3종류 이상을 포함해야 합니다.")
        return new_password1
    
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password1 != new_password2:
            raise forms.ValidationError('두 비밀번호가 일치하지 않습니다.')
        return new_password2
    