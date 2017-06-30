# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
# Create your views here.
def index(request):
    context = {}
    if 'context' in request.session:
        context = request.session['context']
        request.session.pop('context')
    return render(request, 'login/index.html', context)

def login(request):
    login_response = User.objects.login(request.POST)
    if 'login_error' in login_response:
        request.session['context'] = login_response
        return redirect('auth:index')
    request.session['user_id'] = login_response['user_id']
    request.session['user_name'] = login_response['alias']
    print request.session['user_name'] + '*********'
    return redirect('friends:home')

def register(request):
    registration_response = User.objects.register(request.POST)
    if len(request.POST['password']) < 8:
        registration_response['password'] = 'Password must be at least 8 characters'
    request.session['context'] = registration_response
    return redirect('auth:index')

def logout(request):
    request.session.clear()
    return redirect('auth:index')
