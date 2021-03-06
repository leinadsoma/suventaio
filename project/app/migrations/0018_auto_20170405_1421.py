# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20170404_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, help_text='Introduce solo n\xfameros', null=True, verbose_name='Cantidad')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_parent', to='app.Product')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_product', to='app.Product')),
            ],
        ),
        migrations.AddField(
            model_name='sell_point',
            name='invoice_domain',
            field=models.CharField(blank=True, help_text='Dominio de la sucursal', max_length=40, null=True),
        ),
    ]
