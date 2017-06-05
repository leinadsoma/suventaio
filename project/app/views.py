# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from taggit.models import Tag
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.db.models import Q
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.core import serializers
from django.utils.crypto import get_random_string
from forms import *
from models import *
from django.http import JsonResponse
from pprint import pprint
import json
from django.core import serializers
import re
from validate_email import validate_email
from datetime import datetime, timedelta
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context, Template
from django.core.mail import EmailMultiAlternatives, get_connection
from config.settings import DEFAULT_FROM_EMAIL, SITE_ID, PRODUCTION, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS
from django.contrib.auth.decorators import login_required
import urllib
from django.http import Http404 
import time
from serializer import ExtJsonSerializer
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_domain(request):
	domain = request.META['HTTP_HOST'].split('.')[0]
	if domain == 'localhost:8000' or domain == 'zaresapp' or domain == 'suventa':
		domain = 'zaresapp'
	return domain

def user_login(request):
	domain = get_domain(request)
	message_username = ''
	if not request.user.is_anonymous():
		return HttpResponseRedirect(reverse('index',))
	if request.method == "POST":
		if 'login' in request.POST:
			username = request.POST.get('username')	
			password = request.POST.get('password')
			if validate_email(username):
				user = User.objects.filter(email=username)
				if user:
					username = user[0].username
				else:
					message_username = 'Usuario o Contraseña incorrectos'
			else:
				username =  domain + '_' + request.POST.get('username')
			if not message_username:
				access = authenticate(username=username, password=password)
				if access:
					login(request, access)
					return HttpResponseRedirect(reverse('user_login'))
				else:
					username = request.POST.get('username')
					message_username = 'Usuario o Contraseña incorrectos'
	return render(request, 'app/login_user.html',locals())

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('user_login'))

def privacity(request):
	return render(request, 'app/privacity.html',locals())

def landing(request):
	return render(request, 'app/landing.html',locals())

def index(request):
	if request.user.is_anonymous():
		domain = get_domain(request)
		if domain == 'finezipo.com' or 'www.finezipo.com' or 'localhost:8000':
			return render(request, 'zaresapp/finezipo/index.html',locals())
		elif domain == 'vamico.mx.com' or 'www.vamico.mx.com':
			return render(request, 'zaresapp/vamico/index.html',locals())
		elif domain == 'finezipo.com' or 'www.finezipo.com' or 'localhost:8000':
			return render(request, 'zaresapp/finezipo/index.html',locals())
		else:
			return render(request, 'app/landing.html',locals())
	else:
		if request.user.profile == 'Administrador' or request.user.is_superuser:
			return render(request, 'app/index.html',locals())
		elif request.user.profile == 'Cajero' or request.user.profile == 'Vendedor' or request.user.profile == 'Vendedor autorizado para cobrar':
			if len(request.user.sell_point.all()) > 1:
				return HttpResponseRedirect(reverse('select_sellpoint'))
			else:
				if request.user.profile == 'Vendedor' or request.user.profile == 'Vendedor autorizado para cobrar':
					return HttpResponseRedirect(reverse('vendor', args=[request.user.sell_point.all()[0].slug])+'?id='+str(request.user.sell_point.all()[0].id))

def invoice(request):
	form = InvoiceClientForm()
	if request.method == "POST":
		form = InvoiceClientForm(request.POST)
	return render(request, 'app/invoice.html',locals())

@login_required( login_url = '/login/' )
def select_sellpoint(request):
	return render(request, 'app/select_sellpoint.html',locals())

def rest_inventory(product_attr, quantity):
	product_attr.inventory = product_attr.inventory - quantity
	product_attr.save()
	return True

@csrf_exempt
@login_required( login_url = '/login/' )
def vendor(request, slug):
	sell_point = Sell_point.objects.get(id=request.GET.get('id'), slug=slug)
	show_sellpoint_name = True
	if request.method == 'POST':
		if 'get_products' in request.POST:
			return JsonResponse({
				'products': ExtJsonSerializer().serialize( Product_attrs.objects.filter(product__menu=Menu.objects.get(id=request.POST.get('menu')), sell_point=sell_point, active=True), fields=('alias','inventory','price','dynamic_price','bar_code','taxes'), props=('image','name','units','quantity','format_price','color_menu')),
			})
		if 'last_tickets' in request.POST:
			return JsonResponse({
				'tickets': ExtJsonSerializer().serialize( Ticket.objects.filter(user=request.user).order_by('-id')[0:5], fields=('code_sellpoint', 'total'), props=() ),
			})
		if 'make_ticket' in request.POST:
			products_ticket = json.loads(request.POST.get('ticket'))
			anticipe = request.POST.get('anticipe')
			is_order = request.POST.get('is_order')
			ticket = Ticket()
			code_sellpoint, code_company = ticket.assign_codes(sell_point)
			ticket.code_sellpoint = code_sellpoint
			ticket.code_company = code_company
			ticket.sell_point = sell_point
			ticket.user = request.user
			if is_order == 'true':
				ticket.is_order = True
				ticket.anticipe = anticipe
			else:
				ticket.is_order = False
				ticket.anticipe = 0
			if request.user.profile == 'Vendedor':
				ticket.status = 'Pendiente'
			else:
				ticket.status = 'Cobrado'
			ticket.total = 0
			ticket.taxes = 0
			ticket.secret_code = get_random_string(length=8)
			ticket.cut = ticket.assign_cut(sell_point)
			ticket.save()
			total = 0
			taxes = 0
			for product_ticket in products_ticket:
				product_attr = Product_attrs.objects.get(id=product_ticket['product_id'])
				if not ticket.status == 'Pendiente':
					rest_inventory(product_attr, product_ticket['quantity'])
					
					#for products in product_attr.products.recipe.all()
						#try:
							#product_attr.objects.get(products=)
				ticket_products = Ticket_products()
				ticket_products.ticket = ticket
				ticket_products.product = product_attr.product.name
				ticket_products.alias = product_ticket['alias']
				ticket_products.quantity = product_ticket['quantity']
				ticket_products.price = product_ticket['price']
				ticket_products.total = round((float(product_ticket['price']) * float(product_ticket['quantity'])),2)
				if product_attr.taxes:
					ticket_products.taxes = ( ticket_products.total / 1.16) * .16
				else:
					ticket_products.taxes = 0
				ticket_products.save()
				total += ticket_products.total
				taxes += ticket_products.taxes
			ticket.total = total
			ticket.taxes = taxes
			ticket.save()
			return JsonResponse({
				'code': ticket.code_sellpoint,
				'total': total,
				'taxes': taxes,
				'subtotal': total - taxes,
				'key': ticket.secret_code,
			})
	my_products = sell_point.my_products()
	my_menus = sell_point.my_menus(my_products)
	return render(request, 'app/vendor.html',locals()) 

@login_required( login_url = '/login/' )
def users(request):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		users = User.objects.filter(company=request.user.company)
	else:
		raise Http404
	return render(request, 'app/users.html',locals())

@login_required( login_url = '/login/' )
def user_form(request, action):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if action == 'add':
			form = UserForm()
			if request.method == "POST":
				form = UserForm(request.POST)
				if form.is_valid():
					user = form.save(commit=False)
					user.set_password('l6jig7_*po@v152$-k2m@3')
					user.company = request.user.company
					user.username = request.user.company.name.lower() + '_' + user.visible_username
					user.save()
					form.save_m2m()
					return HttpResponseRedirect(reverse('change_password', args=[user.id]))
		elif action == 'edit':
			user = User.objects.get(id=request.GET.get('id'))
			form = UserForm(instance=user)
			if request.method == "POST":
				form = UserForm(request.POST, instance=user)
				if form.is_valid():
					user = form.save(commit=False)
					user.username = request.user.company.name.lower() + '_' + user.visible_username
					user.save()
					form.save_m2m()
					return HttpResponseRedirect(reverse('users'))
		elif action == 'delete':
			User.objects.get(id=request.GET.get('id')).delete()
			return HttpResponseRedirect(reverse('users'))
	else:
		raise Http404
	return render(request, 'app/user_form.html',locals())

@login_required( login_url = '/login/' )
def change_password(request, id):
	user = User.objects.get(id=id)
	if request.user.profile == 'Administrador' or request.user.is_superuser or request.user == user:
		form = Change_PasswordForm(instance=user)	
		if request.method == "POST":
			form = Change_PasswordForm(request.POST, instance=user)
			if form.is_valid():
				user = form.save(commit=False)
				user.set_password(request.POST.get('password2'))
				user.password2 = None
				user.password3 = None
				user.save()
		return render(request, 'app/change_password_form.html',locals())
	else:
		raise Http404

def sellpoints(request):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		pvs = Sell_point.objects.filter(company = request.user.company)
	else:
		raise Http404
	return render(request, 'app/sellpoints.html',locals())

def sellpoint_form(request, acction):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if acction == 'add':
			form = Sell_pointForm()
			if request.method == "POST":
				form = Sell_pointForm(request.POST, request.FILES)
				if form.is_valid():
					points = len(Sell_point.objects.filter(company=request.user.company))
					if points >= request.user.company.sell_point_limits:
						messages.error(request, 'Llegaste al limite de tus puntos de venta')
						return HttpResponseRedirect(reverse('sellpoints'))
					else:
						obj = form.save(commit=False)
						obj.name = obj.name.upper()
						obj.company = request.user.company
						obj.create_by = request.user
						if points == 0:
							obj.cost = 1200
						elif points == 1:
							obj.cost = 800
						elif points > 1:
							obj.cost = 400
						obj.save()
						return HttpResponseRedirect(reverse('sellpoints'))
		elif acction == 'edit':
			sellpoint = Sell_point.objects.get(id=request.GET.get('id'))
			form = Sell_pointForm(instance=sellpoint)
			if request.method == "POST":
				form = Sell_pointForm(request.POST, request.FILES, instance=sellpoint)
				if form.is_valid():
					obj = form.save(commit=False)
					obj.name = obj.name.upper()
					obj.save()
					return HttpResponseRedirect(reverse('sellpoints'))
		elif acction == 'delete':
			Sell_point.objects.get(id=request.GET.get('id')).delete()
			return HttpResponseRedirect(reverse('sellpoints'))	
		return render(request, 'app/sellpoint_form.html',locals())
	else:
		raise Http404

@csrf_exempt
def menus(request):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		menus = Menu.objects.filter(company = request.user.company)
	else:
		raise Http404
	return render(request, 'app/menus.html',locals())

@csrf_exempt
def menu_form(request, acction):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if acction == 'add':
			form = MenusForm(request.user,)
			if request.method == "POST":
				form = MenusForm(request.user, request.POST)
				if form.is_valid():
					obj = form.save(commit = False)
					obj.company = request.user.company
					obj.save()
					return HttpResponseRedirect(reverse('menus'))
		elif acction == 'edit':
			menu = Menu.objects.get(id=request.GET.get('id'))
			form = MenusForm(request.user, instance=menu)
			if request.method == "POST":
				form = MenusForm(request.user, request.POST, instance=menu)
				if form.is_valid():
					obj = form.save(commit = False)
					obj.company = request.user.company
					obj.save()
					return HttpResponseRedirect(reverse('menus'))
		elif acction == 'delete':
			Menu.objects.get(id=request.GET.get('id')).delete()
			return HttpResponseRedirect(reverse('menus'))	
		return render(request, 'app/menu_form.html',locals())
	else:
		raise Http404

@csrf_exempt
def menus_ajax(request):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if 'treeData' in request.POST:
			def recursor (data, parent):
				level = 0
				for d in data:
					menu = Menu.objects.get(id = d['id'])
					menu.nivel = level
					menu.parent = parent
					menu.save()
					if d['children']:
						recursor(d['children'], menu)
					level += 1
			data = json.loads(request.POST.get('treeData'))
			recursor (data, None)
			return JsonResponse({
				'json': True,
			})
		if 'edit' in request.POST:
			menu = Menu.objects.get(id = request.POST.get('id'))
			menu.name = request.POST.get('name')
			menu.color = request.POST.get('color')
			try :
				menu.parent = Menu.objects.get(id = request.POST.get('parent'))
			except:
				menu.parent = None
			menu.save()
			return JsonResponse({
				'json': True,
			})
		if 'getid' in request.POST:
			menu = Menu.objects.get(id = request.POST.get('getid'))
			try:
				parent = menu.parent.id
			except:
				parent = None
			return JsonResponse({
				'id': menu.id,
				'name': menu.name,
				'color': menu.color,
				'parent': parent,
			})
		if 'delete' in request.POST:
			Menu.objects.get(id = request.POST.get('id')).delete()
			return JsonResponse({
				'json': True,
			})
	else:
		raise Http404

def products(request):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		products = Product.objects.filter(company = request.user.company)
		return render(request, 'app/products.html',locals())
	else:
		raise Http404

@csrf_exempt
def product_form(request, acction):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if acction == 'add':
			form = ProductForm(request.user,)
			if request.method == "POST":
				form = ProductForm(request.user, request.POST)
				if form.is_valid():
					obj = form.save(commit = False)
					obj.company = request.user.company
					obj.save()
					form.save_m2m()
					for sell_point in obj.sell_points.all():
						product_attrs = Product_attrs()
						product_attrs.product = obj
						product_attrs.sell_point = sell_point
						product_attrs.alias = obj.name
						product_attrs.save()
					return HttpResponseRedirect(reverse('products'))
		elif acction == 'edit':
			product = Product.objects.get(id=request.GET.get('id'))
			list_sell_points = []
			for sell_point in product.sell_points.all():
				list_sell_points.append(sell_point)
			form = ProductForm(request.user, instance=product)
			if request.method == "POST":
				form = ProductForm(request.user, request.POST, instance=product)
				if form.is_valid():
					obj = form.save(commit = False)
					obj.company = request.user.company
					obj.save()
					form.save_m2m()
					for sell_point in obj.sell_points.all():
						if not Product_attrs.objects.filter(product=product, sell_point=sell_point):
							product_attrs = Product_attrs()
							product_attrs.product = obj
							product_attrs.sell_point = sell_point
							product_attrs.alias = obj.name
							product_attrs.save()
					for sell_point in list_sell_points:
						if not sell_point in obj.sell_points.all():
							Product_attrs.objects.filter(product=product, sell_point=sell_point).delete()
					return HttpResponseRedirect(reverse('products'))
		elif acction == 'delete':
			Product.objects.get(id=request.GET.get('id')).delete()
			return HttpResponseRedirect(reverse('products'))	
		return render(request, 'app/product_form.html',locals())
	else:
		raise Http404

def recipes(request, slug):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		product = Product.objects.get(id=request.GET.get('id'), slug=slug)
		if request.user.company == product.company or request.user.is_superuser:
			recipes = Recipe.objects.filter(parent=product)
			return render(request, 'app/recipes.html',locals())
		else:
			raise Http404
	else:
		raise Http404

def recipe_form(request, acction):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		product = Product.objects.get(id=request.GET.get('id'))
		if request.user.company == product.company or request.user.is_superuser:
			if acction == 'add':
				form = RecipeForm(request.user, product,)
				if request.method == "POST":
					form = RecipeForm(request.user, product, request.POST)
					if form.is_valid():
						obj = form.save(commit = False)
						try:
							recipe = Recipe.objects.get(product=obj.product, parent=product)
							recipe.quantity = recipe.quantity + obj.quantity
							recipe.save()
						except:
							obj.parent = product
							obj.save()
						return HttpResponseRedirect(reverse('recipes', args=[product.slug])+'?id='+str(product.id))
			elif acction == 'delete':
				Recipe.objects.get(id=request.GET.get('recipe')).delete()
				return HttpResponseRedirect(reverse('recipes', args=[product.slug])+'?id='+str(product.id))	
			return render(request, 'app/recipe_form.html',locals())
		else:
			raise Http404
	else:
		raise Http404

def product_attributes(request, slug):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		product = Product.objects.get(id=request.GET.get('id'), slug=slug)
		product_attrs = Product_attrs.objects.filter(product=product)
		
		return render(request, 'app/product_attributes.html',locals())
		
	else:
		raise Http404

def product_attribute_form(request):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		product_attrs = Product_attrs.objects.get(id=request.GET.get('id'))
		if request.user.company == product_attrs.sell_point.company or request.user.is_superuser:
			form = Product_attrsForm(instance = product_attrs)
			if request.method == "POST":
				form = Product_attrsForm(request.POST, instance = product_attrs)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect(reverse('product_attributes', args=[product_attrs.product.slug]) + '?id=' + str(product_attrs.product.id))
			return render(request, 'app/product_attribute_form.html',locals())
		else:
			raise Http404
	else:
		raise Http404

def sellpoints_cut(request):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		pvs = Sell_point.objects.filter(company = request.user.company)
	else:
		raise Http404
	return render(request, 'app/sellpoints_cut.html',locals())

def cut_times(request, slug):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		sellpoint = Sell_point.objects.get(id=request.GET.get('id'), slug=slug)
		cuttime = Cuttime.objects.filter(sell_point=sellpoint)
		if request.user.company == sellpoint.company or request.user.is_superuser:
			return render(request, 'app/cut_times.html',locals())
		else:
			raise Http404
	else:
		raise Http404
	
@csrf_exempt
def cut_time_form(request, slug):
	sellpoint = Sell_point.objects.get(id=request.GET.get('id'), slug=slug)
	try:
		Cuttime.objects.get(id=request.GET.get('delete')).delete()
		return HttpResponseRedirect(reverse('cut_times', args=[sellpoint.slug])+'?id='+str(sellpoint.id))
	except:
		pass
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if request.user.company == sellpoint.company or request.user.is_superuser:
			form = CuttimeForm()
			if request.method == "POST":
				cuttime = Cuttime()
				cuttime.time = datetime.strptime(request.POST.get('time'), '%I:%M %p')
				cuttime.sell_point = sellpoint
				cuttime.save()
				return HttpResponseRedirect(reverse('cut_times', args=[sellpoint.slug])+'?id='+str(sellpoint.id))
			return render(request, 'app/cut_time_form.html',locals())
		else:
			raise Http404
	else:
		raise Http404

def cuts(request, slug):
	sellpoint = Sell_point.objects.get(id=request.GET.get('id'), slug=slug)
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if request.user.company == sellpoint.company or request.user.is_superuser:
			paginator = Paginator(Cut.objects.filter(sell_point = sellpoint).order_by('-id'), 35)
			try:
				cuts = paginator.page(request.GET.get('page'))
			except PageNotAnInteger:
				cuts = paginator.page(1)
			except EmptyPage:
				cuts = paginator.page(paginator.num_pages)
			pagemin = cuts.number - 2
			pagemax = cuts.number + 5
			return render(request, 'app/cuts.html',locals())
		else:
			raise Http404
	else:
		raise Http404

def make_cut(cut):
	cut.terminate = True
	cut.save()
	return True

@csrf_exempt
def cut_details(request):
	cut = Cut.objects.get(id=request.GET.get('id')) 
	if request.method == 'POST':
		if 'make_cut' in request.POST:
			action = make_cut(cut)
			return JsonResponse({
				'cut': action,
			})
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if request.user.company == cut.sell_point.company or request.user.is_superuser:
			products_array = []
			total = 0
			taxes = 0
			tickets = Ticket.objects.filter(cut = cut).order_by('-id')
			ticket_products = Ticket_products.objects.filter(ticket__cut=cut).order_by('alias')
			for ticket_product in ticket_products:
				flag = True
				for row in products_array:
					if row['alias'] == ticket_product.alias and row['price'] == ticket_product.price:
						row['quantity'] += ticket_product.quantity
						row['total'] += ticket_product.total
						row['taxes'] += ticket_product.taxes
						flag = False
						break
				if flag:
					products_array.append( 
						{
							'alias':ticket_product.alias,
							'quantity':ticket_product.quantity,
							'price':ticket_product.price,
							'total':ticket_product.total,
							'taxes':ticket_product.taxes,
						}
					)
				total +=  ticket_product.total
				taxes += ticket_product.taxes
			subtotal = total - taxes
			return render(request, 'app/cut_details.html',locals())
		else:
			raise Http404
	else:
		raise Http404

def ticket_detail(request, id):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		ticket = Ticket.objects.get(id=id)
		if request.user.company == ticket.sell_point.company or request.user.is_superuser:
			return render(request, 'app/ticket_detail.html',locals())
		else:
			raise Http404
	else:
		raise Http404

def invoice_sellpoint(request):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		pvs = Sell_point.objects.filter(company = request.user.company)
	else:
		raise Http404
	return render(request, 'app/invoice_sellpoint.html',locals())

def invoice_sellpoint_form(request, acction):
	if request.user.profile == 'Administrador' or request.user.is_superuser:
		if acction == 'edit':
			sellpoint = Sell_point.objects.get(id=request.GET.get('id'))
			form = InvoiceSell_pointForm(instance=sellpoint)
			if request.method == "POST":
				form = InvoiceSell_pointForm(request.POST, request.FILES, instance=sellpoint)
				if form.is_valid():
					obj = form.save(commit=False)
					obj.rfc = obj.rfc.upper()
					obj.save()
					return HttpResponseRedirect(reverse('invoice_sellpoint'))
		return render(request, 'app/invoice_sellpoint_form.html',locals())
	else:
		raise Http404

####FINEZIPO

def finezipo_nosotros(request):
	return render(request, 'zaresapp/finezipo/nosotros.html',locals())

def finezipo_artistas(request, artista):
	if artista == 'manelyk':
		artista = 'Manelyk'
		return render(request, 'zaresapp/finezipo/manelik.html',locals())
	if artista == 'tracy':
		artista = 'Tracy Sáenz'
		return render(request, 'zaresapp/finezipo/tracy.html',locals())
	if artista == 'jenny':
		artista = 'Jenny Garcia'
		return render(request, 'zaresapp/finezipo/jenny.html',locals())
	if artista == 'gemelos':
		artista = 'GEMELOS'
		return render(request, 'zaresapp/finezipo/gemelos.html',locals())
	if artista == 'sabrinasabrok':
		artista = 'Sabrina Sabrok'
		return render(request,'zaresapp/finezipo/sabrinasabrok.html',locals())
	if artista == 'lorena':
		artista = 'Lorena Herrera'
		return render(request,'zaresapp/finezipo/lorena.html',locals())
	if artista == 'esteban':
		artista = 'Esteban Martinez'
		return render(request,'zaresapp/finezipo/esteban.html',locals())
	if artista == 'elettra':
		artista = 'Elettra Lamborghini'
		return render(request,'zaresapp/finezipo/elettra.html',locals())
	if artista == 'igor':
		artista = 'Igor'
		return render(request,'zaresapp/finezipo/igor.html',locals())
	if artista == 'fernando':
		artista = 'Fernando'
		return render(request,'zaresapp/finezipo/fernando.html',locals())
	if artista == 'jawi':
		artista = 'Jawi'
		return render(request,'zaresapp/finezipo/jawi.html',locals())
	if artista == 'vanessa':
		artista = 'Vanessa Claudio'
		return render(request,'zaresapp/finezipo/vanessa.html',locals())
	if artista == 'lisvega':
		artista = 'Lis Vega'
		return render(request,'zaresapp/finezipo/lisvega.html',locals())
	if artista == 'marlenefavela':
		artista = 'MAarlene Favela'
		return render(request,'zaresapp/finezipo/marlenefavela.html',locals())
	if artista == 'vanessahuppenkothen':
		artista = 'Vanessa Huppenkothen'
		return render(request,'zaresapp/finezipo/vanessahuppenkothen.html',locals())
	if artista == 'talia':
		artista = 'Talia Acashore'
		return render(request,'zaresapp/finezipo/talia.html',locals())

def finezipo_contacto(request):
	if request.method == "POST":
		nombre = request.POST.get('nombre')
		email = request.POST.get('email')	
		empresa = request.POST.get('empresa')
		mensaje = request.POST.get('mensaje')
		subject, from_email, to = 'Contacto Finezipo', 'finezipo@zaresapp.com <FineZipo>', 'rampzodia1@gmail.com'
		text_content = 'TIENES UNA NUEVA FORMA DE CONTACTO'
		html_content = '<h2>TIENES UNA NUEVA FORMA DE CONTACTO</h2>'+'<p><strong>Nombre:</strong> ' + unicode(nombre) + '</p>'+'<p><strong>Email:</strong> ' + unicode(email) + '</p>'+'<p><strong>Empresa:</strong> ' + unicode(empresa) + '</p>'+'<p><strong>Mensaje:</strong> ' + unicode(mensaje) + '</p>'
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		mensaje = "Nos pondremos pronto en contacto contigo. :)"
	return render(request, 'zaresapp/finezipo/contacto.html',locals())

def finezipo_que_hacemos(request):
	return render(request, 'zaresapp/finezipo/que_hacemos.html',locals())

def finezipo_shows(request):
	return render(request, 'zaresapp/finezipo/shows.html',locals())


####VAMICO

