from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserChangeCustomForm(UserChangeForm):
    password = ''
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email',]