from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages


# Create your views here.

def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'you have registered, log in to your account')
        return redirect('bonausers:login')
    return render(request, 'signup.html', {'form': form})


def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'authenticated')
        return redirect('bonaapp:home_page')
    return render(request, 'login.html')


def sign_out(request):
    logout(request)
    return redirect('bonausers:login')


def profile(request):
    form = ChangePasswordForm(request.user, request.POST)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('bonausers:profile')
    form = ChangePasswordForm(request.user)
    return render(request, 'profile.html', {'form': form})
