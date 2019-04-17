from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, update_session_auth_hash
from django.contrib.auth import (login as django_login, logout as django_logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .form import UserChangeCustomForm

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form = form.save()
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
    
def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = {
        'people': people,
    }
    return render(request, 'accounts/people.html', context)

@login_required
def edit_account(request):
    if request.method == 'POST':
        form = UserChangeCustomForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('people', request.user.username)
    form = UserChangeCustomForm(instance=request.user)
    context = {
        'edit_form': form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def del_account(request):
    if request.method == 'POST':
        request.user.delete()
    return redirect('posts:list')

@login_required
def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form = form.save()
            update_session_auth_hash(request, form)
            return redirect('people', request.user.username)
    form = PasswordChangeForm(user=request.user)
    context = {
        'password_form': form
    }
    return render(request, 'accounts/form.html', context)