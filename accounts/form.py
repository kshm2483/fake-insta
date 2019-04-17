from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile

class UserChangeCustomForm(UserChangeForm):
    password = ''
    class Meta:
        model = get_user_model()
        fields = ['last_name', 'first_name', 'email',]
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'introduction',]