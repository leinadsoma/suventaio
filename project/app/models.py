# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField
from django.utils import timezone
from django.db.models import Q
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
import random
import datetime
from config.settings import MEDIA_URL, STATIC_URL
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Transpose, SmartResize
from imagekit import ImageSpec, register
from django.http import Http404
import re
from bs4 import BeautifulSoup
from slugify import slugify
import urllib
import time
import json
from mptt.models import MPTTModel, TreeForeignKey

class Company(models.Model):
    name = models.CharField(max_length=250, unique=True)
    sell_point_limits = models.IntegerField(default=5)
    creation_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']

User_Profile = (
        ('Administrador','Administrador'),
        ('Vendedor','Vendedor'),
        ('Cajero','Cajero'),
        ('Cajero y Vendedor','Cajero y Vendedor'),
        ('Vendedor autorizado para cobrar','Vendedor autorizado para cobrar'),
        ('Supervisor','Supervisor'),
    )

def pathuser_photo(self, filename):
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    upload_to = "media/users/%s/profile_picture/%s/%s" % (self.username, date, filename)
    return upload_to

class User(AbstractUser):
    visible_username = models.CharField('Nombre de Usuario', max_length=250)
    company = models.ForeignKey('Company', blank=True, null=True, related_name='user_company')
    sell_point = models.ManyToManyField('Sell_point', blank=True, verbose_name="Asignado a Puntos de Venta:")
    profile = models.CharField(max_length=250, choices=User_Profile, default='Vendedor', verbose_name="Tipo de perfil")
    password2 = models.CharField('Password', default=None, blank=True, null=True, max_length=144, help_text="Ingresa un password")
    password3 = models.CharField('Password otra vez', default=None, blank=True, null=True, max_length=144, help_text="Ingresa de nuevo el mismo password")
    avatar = ProcessedImageField(verbose_name="Foto de Perfil", blank=True, null=True, upload_to=pathuser_photo, processors=[ResizeToFill(300, 300)],format='JPEG', options={'quality': 60})
    
    def __unicode__(self):
        return self.username

def path_logos(self, filename):
    date = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    upload_to = "media/%s/logo/%s%s" % (self.company.name, date, filename)
    return upload_to

def path_invoice(self, filename):
    date = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    upload_to = "media/%s/invoice/%s%s" % (self.company.name, date, filename)
    return upload_to

class Sell_point(models.Model):
    name = models.CharField('Nombre del punto de venta', max_length=250, help_text="Ingresa un nombre para definir un Punto de Venta")
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('Company', related_name='sell_point_company')
    depend_to = models.ForeignKey('Sell_point', blank=True, null=True, related_name='sell_point_depend_to', on_delete=models.SET_NULL)
    create_by = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET_NULL, related_name='sell_point_create_by')
    logo = ProcessedImageField(blank=True, null=True, upload_to=path_logos, processors=[ResizeToFill(400, 400)],format='JPEG',options={'quality': 60}, help_text='Puedes agregar una foto a tu punto de venta <br /> <small><small>Debe ser menor a 300kb</small></small>')
    pay_date = models.DateField(blank=True, null=True, auto_now_add=True)
    cost = models.FloatField(blank=True, null=True)
    slug = AutoSlugField(populate_from='name', always_update=True)
    address_1 = models.CharField('Direccion Linea 1', max_length=40, help_text="1ra linea del ticket", blank=True, null=True)
    address_2 = models.CharField('Direccion Linea 2', max_length=40, help_text="2da linea del ticket", blank=True, null=True)
    address_3 = models.CharField('Direccion Linea 3', max_length=40, help_text="3ra linea del ticket", blank=True, null=True)
    phone = models.CharField('Teléfono', max_length=13, help_text="Teléfono de la sucursal", blank=True, null=True)
    email = models.CharField('Email', max_length=20, help_text="Email de la sucursal", blank=True, null=True)
    domain = models.CharField('Dominio', max_length=40, help_text="Dominio de la sucursal", blank=True, null=True)
    invoice_domain = models.CharField('URL de Facturación', max_length=40, help_text="Dominio de la sucursal para facturar", blank=True, null=True)
    invoice = models.BooleanField('Emites Facturas?', default=False)
    sello = models.FileField('Sello fiscal para hacer facturas <small>(Solo si emites facturas)</small>', blank=True, null=True, upload_to=path_invoice,)
    timbres = models.IntegerField(blank=True, null=True)
    rfc = models.CharField('RFC', max_length=12, blank=True, null=True)
    regimen_fiscal = models.CharField('Regimen Fiscal', max_length=250, blank=True, null=True)
    nombre_fiscal = models.CharField('Nombre Fiscal', max_length=250, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def my_products(self):
        return Product_attrs.objects.filter(sell_point = self, active=True)

    def my_menus(self, products_attrs):
        menus = []
        for product_attrs in products_attrs:
            for menu in product_attrs.product.menu.get_ancestors(ascending=False, include_self=True):
                if not menu in menus:
                    menus.append(menu.id)
        return Menu.objects.filter(id__in=menus)

    def len_cuttime(self):
        return len(Cuttime.objects.filter(sell_point=self))

    def cuttimes(self):
        return Cuttime.objects.filter(sell_point=self)

    def last_cut(self):
        try:
            return Cut.objects.filter(terminate=True, sell_point=self).order_by('-id')[0]
        except:
            return False

    def actual_cut(self):
        try:
            return Cut.objects.get(terminate=False, sell_point=self)
        except:
            return False

class Menu(MPTTModel):
    name = models.CharField('Nombre del menu:', max_length=250)
    color = models.CharField('Color de los botones', default="#5090c1", max_length=250,)
    company = models.ForeignKey('Company')
    parent = TreeForeignKey('self', verbose_name='Depende de?', null=True, blank=True, related_name='children', db_index=True, help_text="Este menú depende de algún otro?")
    slug = AutoSlugField(populate_from='name', always_update=True)
    nivel = models.PositiveIntegerField(default=1)

    def __unicode__(self) :
        return '%s' % (self.name)

    class MPTTMeta:
        order_insertion_by = ['nivel']

    class Meta:
        ordering = ["nivel"]

def path_image_product(self, filename):
        date = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        upload_to = "media/%s/products/%s/%s%s" % (self.menu.company.name, name, date, filename)
        return upload_to

Units = (
    ('Unidades','Unidades'),
    ('Kilogramos','Kilogramos'),
    ('Gramos','Gramos'),
    ('Litros','Litros'),
    ('Mililitros','Mililitros'),
    ('Onzas','Onzas'),
)

class Product(models.Model):
    image = ProcessedImageField(verbose_name='Imagen del producto', blank=True, null=True, upload_to=path_image_product, processors=[ResizeToFill(200, 200)],format='JPEG',options={'quality': 40}, help_text='Puedes asociar una imagen a cada producto <br /> <small><small>Debe ser menor a 300kb</small></small>')
    name = models.CharField('Nombre del producto', max_length=250, help_text="Introduce el nombre del producto")
    units = models.CharField('Unidades', choices=Units, blank=True, null=True, max_length=250, help_text="Selecciona el tipo de unidades")
    quantity = models.IntegerField('Cantidad', blank=True, null=True, help_text="Introduce solo números")
    slug = AutoSlugField(populate_from='name', always_update=True)
    company = models.ForeignKey('Company')
    sell_points = models.ManyToManyField('Sell_point', blank=True, related_name='product_sell_points', verbose_name="Se vende en:")
    menu = TreeForeignKey('Menu', verbose_name='Menu del producto', null=True, blank=True, related_name='product_menu', db_index=True, help_text="Selecciona el menú del que depende este producto.s")

    def __unicode__(self) :
        return '%s [%s]' % (self.name, self.units)

    def len_sell_points(self):
        return len(self.sell_points.all())

    def full_name(self):
        return str(self.quantity) + ' ' + self.units + ' ' + self.name

    def len_recipe(self):
        return len(Recipe.objects.filter(parent=self))

    def recipe(self):
        return Recipe.objects.filter(parent=self)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "menu")

class Recipe(models.Model):
    quantity = models.IntegerField('Cantidad de producto', blank=True, null=True, help_text="Introduce solo números")
    product = models.ForeignKey('Product', related_name='recipe_product', verbose_name="Elige un producto de la lista")
    parent = models.ForeignKey('Product', related_name='recipe_parent')


class Product_attrs(models.Model):
    product = models.ForeignKey('Product', related_name='product_attrs_points')
    sell_point = models.ForeignKey('Sell_point', related_name='product_attrs_points')
    alias = models.CharField('Alias del producto', max_length=30, blank=True, help_text="Nombre del producto que aparecerá en el ticket")
    inventory = models.IntegerField('Inventario de producto en este punto de venta', default=0, help_text="Cantidad de producto en el sistema")
    price = models.FloatField('Precio del producto', default=0, help_text="Precio final de venta al público" )
    taxes = models.BooleanField('I.V.A.', default=False, help_text="A este producto se le graba IVA?" )
    dynamic_price = models.BooleanField('Precio dinámico',default=False, help_text="Habilita esta opción si el precio lo pueden cambiar los vendedores")
    bar_code = models.CharField('Codigo de barras', max_length=35, default=None, blank=True, null=True)
    primary = models.BooleanField('Es principal?', default=False, help_text="Quieres resaltar este producto?")
    active = models.BooleanField('Esta activo?', default=True, help_text='Este producto aparece en el sistema?')

    def __unicode__(self) :
        return '%s' % (self.product.name)

    def image(self):
        if self.product.image:
            return self.product.image
        else:
            return False

    def name(self):
        if self.product.name:
            return self.product.name
        else:
            return False

    def units(self):
        if self.product.units:
            return self.product.units
        else:
            return False

    def quantity(self):
        if self.product.quantity:
            return self.product.quantity
        else:
            return False

    def format_price(self):
        return '$ ' + str(round( self.price, 2))

    def color_menu(self):
        return self.product.menu.color

Status_ticket = (
    ('Pendiente', 'Pendiente'),
    ('Cobrado', 'Cobrado'),
    ('Cortado', 'Cortado'),
)

class Ticket(models.Model):
    code_sellpoint = models.IntegerField()
    code_company = models.IntegerField()
    sell_point = models.ForeignKey('Sell_point', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50,choices=Status_ticket, default="Pendiente")
    date = models.DateTimeField(auto_now_add=True)
    cut = models.ForeignKey('Cut', null=True, blank=True, on_delete=models.SET_NULL)
    total = models.FloatField(default=0)
    taxes = models.FloatField(default=0)
    invoice = models.BooleanField(default=False)
    secret_code = models.CharField(max_length=8, default='')
    anticipe = models.FloatField(default=0)
    is_order = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    def assign_cut(self, sell_point):
        cut = Cut.objects.filter(sell_point = sell_point, terminate=False)
        if not cut:
            cut = Cut.objects.filter(sell_point = sell_point).order_by('-code_sellpoint')
            if cut:
                code_sellpoint = cut[0].code_sellpoint + 1 
            else:
                code_sellpoint = 1
            cut = Cut.objects.filter(sell_point__company = sell_point.company).order_by('-code_company')
            if cut:
                code_company = cut[0].code_company + 1 
            else:
                code_company = 1
            cut = Cut()
            cut.code_sellpoint = code_sellpoint
            cut.code_company = code_company
            cut.sell_point = self.sell_point
            cut.save()
            return cut
        else:
            return cut[0]

    def assign_codes(self, sell_point):
        ticket = Ticket.objects.filter(sell_point = sell_point).order_by('-code_sellpoint')
        if not ticket:
            code_sellpoint = 1
        else:
            code_sellpoint = ticket[0].code_sellpoint + 1
        ticket = Ticket.objects.filter(sell_point__company = sell_point.company).order_by('-code_company')
        if not ticket:
            code_company = 1
        else:
            code_company = ticket[0].code_company + 1
        return code_sellpoint, code_company

    def ticket_products(self):
        return Ticket_products.objects.filter(ticket = self)

    def sellpoint_code(self):
        return str(self.code_sellpoint).zfill(11)

    def company_code(self):
        return str(self.code_company).zfill(11)

    def subtotal(self):
        return self.total-self.taxes

class Ticket_products(models.Model):
    ticket = models.ForeignKey('Ticket')
    product = models.CharField(max_length=40)
    alias = models.CharField(max_length=40)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    total = models.FloatField(default=0)
    taxes = models.FloatField(default=0)

class Cut(models.Model):
    code_sellpoint = models.IntegerField()
    code_company = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    sell_point = models.ForeignKey('Sell_point', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    terminate = models.BooleanField(default=False)
    init_time = models.DateTimeField(auto_now_add=True)

    def tickets(self):
        return Ticket.objects.filter(cut=self)

    def total(self):
        tickets = Ticket.objects.filter(cut=self)
        total = 0
        for ticket in tickets:
            total += ticket.total
        return total

    def len_tickets(self):
        return len(Ticket.objects.filter(cut=self))

    def total_taxes(self):
        tickets = Ticket.objects.filter(cut=self)
        total = 0
        for ticket in tickets:
            total += ticket.taxes
        return total

    def last_time(self):
        try:
            return Ticket.objects.filter(cut=self).order_by('-id')[0].date
        except:
            return '-'

class Cuttime(models.Model):
    sell_point = models.ForeignKey('Sell_point')
    time = models.TimeField('Hora de corte', help_text="Ingresa el horario en el que se hara el corte.")

class InvoiceClient(models.Model):
    rfc = models.CharField('RFC', max_length=250, help_text="RFC de la empresa")
    razon_social = models.CharField('Razon social', max_length=250, help_text="Razón social de la empresa")
    telefono = models.CharField('Teléfono', blank=True, null=True, max_length=250, )
    contacto = models.CharField('Nombre de contacto', max_length=250, help_text="Nombre del contacto que requiere la factura")
    email_contacto = models.CharField('Email de contacto', max_length=250, help_text="Email para enviar la factura timbrada")
    calle = models.CharField('Calle', blank=True, null=True, max_length=250)
    numero_exterior = models.CharField('Numero exterior', blank=True, null=True, max_length=250)
    numero_interior = models.CharField('Numero interior', blank=True, null=True, max_length=250)
    colonia = models.CharField('Colonia', blank=True, null=True, max_length=250)
    municipio_o_delegacion = models.CharField('Delegación o Municipio', blank=True, null=True, max_length=250)
    estado = models.CharField('Estado', blank=True, null=True, max_length=250)
    codigo_postal = models.CharField('Codigo Postal', blank=True, null=True, max_length=250)
    pais = models.CharField('Pais', blank=True, null=True, max_length=250)
