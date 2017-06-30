# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from login.models import User

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        friend_list = User.objects.get(id = request.session['user_id']).friends.all()
        if len(friend_list) == 0:
            are_friends = False
        else:
            are_friends = True
        others = []
        users = User.objects.all().exclude(id = request.session['user_id'])
        for user in users:
            if not user in friend_list:
                others.append(user)
        context = {
            'user_name' : request.session['user_name'],
            'my_friends': friend_list,
            'others' : others,
            'are_friends' : are_friends
        }
        return render(request,'friends/home.html', context)
    else:
        return redirect('auth:index')

def add(request):
    if 'user_id' in request.session:
        User.objects.add_friend(request.POST['friend_id'], request.session['user_id'])
        return redirect('friends:home')
    else:
        return redirect('auth:index')

def remove(request, friend_id):
    if 'user_id' in request.session:
        User.objects.remove_friend(friend_id, request.session['user_id'])
        return redirect('friends:home')
    else:
        return redirect('auth:index')

def user(request, user_id):
    if 'user_id' in request.session:
        context = {
            'user' : User.objects.get(id = user_id)
        }
        return render(request, 'friends/user.html', context)
    else:
        return redirect('auth:index')
