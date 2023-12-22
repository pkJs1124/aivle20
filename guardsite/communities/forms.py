from django import forms
from .models import Notice,Comment

class NoticeForm(forms.ModelForm):
    
    class Meta:
        model = Notice
        fields = ('title','content',)
        
# class CommentForm(forms.ModelForm):
    
#     class Meta:
#         model = Comment
#         fields = ('content',)