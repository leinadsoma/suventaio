# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20170405_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='recipe',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_product', to='app.Product', verbose_name='Elige un producto de la lista'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='quantity',
            field=models.IntegerField(blank=True, help_text='Introduce solo n\xfameros', null=True, verbose_name='Cantidad de producto'),
        ),
    ]
