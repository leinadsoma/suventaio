# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *
from forms import *
from taggit.models import Tag
from django import forms
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission
from mptt.admin import MPTTModelAdmin

from .models import User

def permission_unicode(self):
    return  u'%s' % (self.name,)
Permission.__unicode__ = permission_unicode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = False
    search_fields = ('username','email', 'visible_username')
    list_filter = ('company','is_active')
    filter_horizontal = ('user_permissions',)
    fieldsets = (
        ('Usuario', {'fields': ('username', 'visible_username', 'email', 'profile', 'password',)}),
        ('Cuenta', {'fields': ('company','sell_point',)}),
        ('Permisos', {'fields': ('user_permissions',)}),
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','sell_point_limits',)
    search_fields = ('name',)

@admin.register(Sell_point)
class Sell_pointAdmin(admin.ModelAdmin):
    list_display = ('name','creation_date','company','pay_date','cost',)
    search_fields = ('name',)

@admin.register(Product_attrs)
class Product_attrsAdmin(admin.ModelAdmin):
    list_display = ('product','sell_point',)
    search_fields = ('product_name',)

@admin.register(Cut)
class CutAdmin(admin.ModelAdmin):
    pass

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

@admin.register(Ticket_products)
class Ticket_productsAdmin(admin.ModelAdmin):
    pass

@admin.register(Cuttime)
class CuttimeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Menu, MPTTModelAdmin)