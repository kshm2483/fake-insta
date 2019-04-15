from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import (login as django_login, logout as django_logout)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            django_login(request, form)
            return redirect('posts:list')
    else:
        form = UserCreationForm()
    
    context = {
        'sign_form': form
    }
    return render(request, 'accounts/signup.html', context)

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             django_login(request, user)
#             return redirect(request.POST.get('next') or'posts:list')

#     form = AuthenticationForm()
#     context = {
#         'log_form': form,
#         'next': request.GET.get('next', ''),
#     }
#     return render(request, 'accounts/login.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            django_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        form = AuthenticationForm()
    context = {
        'log_form':form,
        'next':request.GET.get('next', ''),
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    django_logout(request)
    return redirect('posts:list')