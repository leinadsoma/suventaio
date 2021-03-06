# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20170331_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cut',
            name='time',
        ),
        migrations.AddField(
            model_name='cut',
            name='init_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cuttime',
            name='time',
            field=models.TimeField(help_text='Ingresa el horario en el que se hara el corte.', verbose_name='Hora de corte'),
        ),
    ]
