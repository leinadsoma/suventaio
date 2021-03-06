# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 20:56
from __future__ import unicode_literals

from django.db import migrations, models
import imagekit.models.fields
import project.app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170323_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=project.app.models.pathuser_photo),
        ),
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(blank=True, default=None, help_text='Ingresa un password', max_length=144, null=True, verbose_name='Password'),
        ),
        migrations.AddField(
            model_name='user',
            name='password3',
            field=models.CharField(blank=True, default=None, help_text='Ingresa de nuevo el mismo password', max_length=144, null=True, verbose_name='Password otra vez'),
        ),
    ]
