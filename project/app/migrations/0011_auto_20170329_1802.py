# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 00:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20170324_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_sellpoint', models.IntegerField()),
                ('code_company', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('terminate', models.BooleanField(default=False)),
                ('sell_point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Sell_point')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_sellpoint', models.IntegerField()),
                ('code_company', models.IntegerField()),
                ('status', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Cobrado', 'Cobrado'), ('Cortado', 'Cortado')], default='Pendiente', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total', models.FloatField(default=0)),
                ('taxes', models.FloatField(default=0)),
                ('invoice', models.BooleanField(default=False)),
                ('secret_code', models.CharField(default='', max_length=8)),
                ('cut', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Cut')),
                ('sell_point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Sell_point')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket_products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=40)),
                ('alias', models.CharField(max_length=40)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('taxes', models.FloatField(default=0)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Ticket')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.CharField(choices=[('Administrador', 'Administrador'), ('Vendedor', 'Vendedor'), ('Cajero', 'Cajero'), ('Cajero y Vendedor', 'Cajero y Vendedor'), ('Vendedor autorizado para cobrar', 'Vendedor autorizado para cobrar'), ('Supervisor', 'Supervisor')], default='Vendedor', max_length=250, verbose_name='Tipo de perfil'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cut',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
