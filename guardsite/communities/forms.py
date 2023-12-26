from django import forms
from .models import Notice,Comment

class NoticeForm(forms.ModelForm):
    
    title = forms.CharField(
        label='제목',
        max_length=30,
        widget=forms.TextInput(
            attrs = {
                'class' : 'my-title',
                'placeholder':'Enter the title'
            }
        )
    )
    
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class' :'my-content',
                'placeholder': 'Enter the content',
                'row':5,
                'cols':40
            }
        )
    )
    class Meta:
        model = Notice
        fields = ('title','content',)
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='댓글 내용',
        widget=forms.Textarea(
            attrs={
                'class': 'my-comment-content',
                'placeholder': '댓글을 입력하세요',
                'rows': 3,
                'cols': 30
            }
        )
    )
    class Meta:
        model = Comment
        fields = ['content']