# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import UserRegisterForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


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
