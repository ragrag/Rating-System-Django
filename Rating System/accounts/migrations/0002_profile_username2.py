# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-24 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username2',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
