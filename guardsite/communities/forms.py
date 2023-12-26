from django import forms
from .models import Notice,Comment

class NoticeForm(forms.ModelForm):
    
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