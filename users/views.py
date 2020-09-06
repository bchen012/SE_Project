# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)

            return redirect('main')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def users_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(username=username)
    context = {'profile': profile,
               'user': user,
               }
    return render(request, 'users/users_profile.html', context)


@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'users/users_profile.html', context)
