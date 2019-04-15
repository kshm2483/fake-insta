from django import forms
from .models import Post, Image, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content',]
        widgets = {'content': forms.TextInput(attrs={
                                                    'placeholder': '내용을 입력하세요.',
                                                    'class': 'content',}),
        }

class ImageForm(forms.ModelForm):
    # file = forms.ImageField(widgets=forms.FileInput(attrs={'multiple':True,}))
    class Meta:
        model = Image
        fields = ['file',]
        widgets = {'file': forms.FileInput(attrs={
                                                'multiple':True, }),
        }
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(label="")
    class Meta:
        model = Comment
        fields = ['content',]
        widgets = {'content': forms.TextInput(attrs={
                                                    'placeholder': '내용을 입력하세요.',
                                                    'class': 'content',}),
        }