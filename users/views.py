# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, Post


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

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user': user,
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/users_profile.html', context)


def unfavorite(request, id):
    post = get_object_or_404(Post, id=id)
    profile = Profile.objects.get(user=request.user)
    profile.favorites.remove(post)
    return redirect('profile')