from django import forms
from .models import Post, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content',]
        widgets = {'content': forms.TextInput(attrs={
                                                    'placeholder': '내용을 입력하세요.',
                                                    'class': 'content',}),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file',]
        widgets = {'file': forms.FileInput(attrs={
                                                'multiple':True, }),
        }