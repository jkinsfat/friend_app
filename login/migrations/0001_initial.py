# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 19:18
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import login.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, validators=[login.models.validate_word])),
                ('alias', models.CharField(max_length=25, unique=True, validators=[login.models.validate_word])),
                ('email', models.CharField(max_length=25, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('password', models.CharField(max_length=125, validators=[login.models.validate_password])),
                ('birth_date', models.DateField(validators=[login.models.validate_before_today])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('friends', models.ManyToManyField(related_name='_user_friends_+', to='login.User')),
            ],
        ),
    ]
