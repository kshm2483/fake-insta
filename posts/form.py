from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image',]
        widgets = {'content': forms.TextInput(attrs={
                                                    'placeholder': '내용을 입력하세요.',
                                                    'class': 'content',}),
        }
