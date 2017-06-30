# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from datetime import date
import bcrypt
import re

def validate_before_today(value):
    if date.today() < value:
        raise ValidationError('Birth date must be before today')

def validate_word(value):
    if len(value) < 3:
        raise ValidationError('Field must be longer than two character')
    pattern = re.compile("[A-Za-z\s]+$")
    match = pattern.match(value)
    if not match:
        raise ValidationError('Field must contain only letters')

def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters')

class UserManager(models.Manager):
    def register(self, register_data):
        response = {}
        if register_data['password'] != register_data['password_confirm']:
            response['password_confirm'] = 'Does not match password'
        hashed = bcrypt.hashpw(register_data['password'].encode(), bcrypt.gensalt())
        new_user = User(
            name=register_data['name'],
            alias=register_data['alias'],
            email=register_data['email'],
            birth_date=register_data['birth_date'],
            password=hashed
        )
        try:
            new_user.full_clean()
            new_user.save()
            response['result'] = 'Registration complete! Try logging in'
        except ValidationError as errors:
            for column_name in errors:
                print "*********8" + column_name[0]
                if column_name[1][0] == "'' value has an invalid date format. It must be in YYYY-MM-DD format.":
                    response[column_name[0]] = "Birth Date cannot be blank"
                else:
                    response[column_name[0]] = column_name[1][0]
            response['result'] = 'Registration incomplete, correct errors above'
        return response

    def login(self, login_data):
        response = {}
        if login_data['login_email'] == '' or login_data['login_password'] == '':
            response['login_error'] = 'Fields cannot be empty'
        else:
            try:
                user_account = User.objects.filter(email=login_data['login_email'])[0]
                hashed = bcrypt.hashpw(login_data['login_password'].encode(), user_account.password.encode())
                if user_account.password == hashed:
                    response['user_id'] = user_account.id
                    response['alias'] = user_account.alias
                else:
                    raise ValidationError
            except:
                response['login_error'] = 'One of these fields is incorrect'
        return response

    def add_friend(self, friend_id, user_id):
        user = User.objects.get(id=user_id)
        new_friend = User.objects.get(id = friend_id)
        user.friends.add(new_friend)

    def remove_friend(self, friend_id, user_id):
        user = User.objects.get(id=user_id)
        old_friend = User.objects.get(id = friend_id)
        user.friends.remove(old_friend)

class User(models.Model):
    name = models.CharField(max_length=25, validators=[validate_word])
    alias = models.CharField(max_length=25, unique=True, validators=[validate_word])
    email = models.CharField(max_length=25, unique=True, validators=[validate_email])
    password = models.CharField(max_length=125, validators=[validate_password])
    birth_date = models.DateField(validators=[validate_before_today])
    friends = models.ManyToManyField("self")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    objects = UserManager()
