# -*- encoding: utf-8 -*-
from django import forms
from models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.utils.translation import ugettext, ugettext_lazy as _

class MaterialColorWidget(widgets.TextInput):
    def render(self, name, value, attrs=None):
        return mark_safe(u""" 
                <div class="cp-container">
                    <div class="input-group form-group">
                        <span class="input-group-addon"><i
                                class="zmdi zmdi-invert-colors"></i></span>
                        <div class="fg-line dropdown">
                            %s
                            <div class="dropdown-menu">
                                <div class="color-picker" data-cp-default="#03A9F4"></div>
                            </div>
                            <i class="cp-value"></i>
                        </div>
                        <i class='fa fa-circle color-menu' color='#5090c1' style='color:#5090c1;margin-left:5px;'></i> 
                        <i class='fa fa-circle color-menu' color='#7d6eb0' style='color:#7d6eb0;margin-left:5px;'></i> 
                        <i class='fa fa-circle color-menu' color='#82af6f' style='color:#82af6f;margin-left:5px;'></i>  
                        <i class='fa fa-circle color-menu' color='#ff965c' style='color:#ff965c;margin-left:5px;'></i>  
                        <i class='fa fa-circle color-menu' color='#e04140' style='color:#e04140;margin-left:5px;'></i>  
                        <i class='fa fa-circle color-menu' color='#ffc557' style='color:#ffc557;margin-left:5px;'></i> 
                        <i class='fa fa-circle color-menu' color='#ce6f9e' style='color:#ce6f9e;margin-left:5px;'></i>
                    </div>
                </div>
            """% (super(MaterialColorWidget, self).render(name, value, attrs)))

class TimeWidget(widgets.TimeInput):
    def render(self, name, value, attrs=None):
        return mark_safe(u""" 
            <div class="input-group form-group">
                <span class="input-group-addon"><i class="zmdi zmdi-time"></i></span>
                <div class="dtp-container">
                    %s
                </div>
            </div>
            """% (super(TimeWidget, self).render(name, value, attrs)))


class MaterialCheckboxWidget(widgets.CheckboxInput):
    def render(self, name, value, attrs=None):
        return mark_safe(u"""%s<i class="input-helper"></i>""" % (super(MaterialCheckboxWidget, self).render(name, value, attrs)))

class LoginForm(forms.ModelForm):
    company = forms.CharField( widget=forms.TextInput(attrs={'class':'input-hidden', 'type':'text'}) )
    class Meta:
        model = User
        fields = ('username','password')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Tu usuario', 'type':'text', 'autofocus':'True'}),
            'password':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Tu contraseña','type':'password'}),
            }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('visible_username','email','avatar','profile','sell_point','is_active',)
        widgets={
            'profile':forms.Select(attrs={'class':'select form-control chosen',}),
            'is_active':MaterialCheckboxWidget(attrs={'class':'select form-control', 'style':'display:none;'}),
            'sell_point':forms.SelectMultiple(attrs={'class':'select form-control chosen','data-placeholder':"Selecciona uno o varios productos..."}),
        }

class Change_PasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password2','password3',)
        widgets={
            'password2':forms.TextInput(attrs={'class':'form-control','required':'required','type':'password'}),
            'password3':forms.TextInput(attrs={'class':'form-control','required':'required','type':'password'}),
        }

class Sell_pointForm(forms.ModelForm):
    class Meta:
        model = Sell_point
        fields = ('name','logo','address_1','address_2','address_3','phone','email',)

class InvoiceSell_pointForm(forms.ModelForm):
    class Meta:
        model = Sell_point
        fields = ('invoice','nombre_fiscal','regimen_fiscal','rfc','sello',)
        widgets={
            'invoice':MaterialCheckboxWidget(attrs={'class':'select form-control', 'style':'display:none;'}),
        }

class InvoiceClientForm(forms.ModelForm):
    class Meta:
        model = InvoiceClient
        fields = ('rfc','razon_social','telefono','contacto','email_contacto','calle','numero_exterior','numero_interior','colonia','municipio_o_delegacion','estado','codigo_postal','pais',)

class MenusForm(forms.ModelForm):
    def __init__(self,user,*args,**kwargs):
        super (MenusForm,self ).__init__(*args,**kwargs)
        self.fields['parent'].queryset = Menu.objects.filter(company = user.company)
    class Meta:
        model = Menu
        fields = ('name','parent','color')
        widgets={
            'color':MaterialColorWidget(attrs={'class':'form-control cp-value', 'value': '#03A9F4', 'type':'text', 'data-toggle':'dropdown'}),
            'parent':forms.Select(attrs={'class':'select form-control chosen',}),
            }

class RecipeForm(forms.ModelForm):
    def __init__(self,user,product,*args,**kwargs):
        super (RecipeForm,self ).__init__(*args,**kwargs)
        self.fields['product'].queryset = Product.objects.filter(company = user.company).exclude(id=product.id)
    class Meta:
        model = Recipe
        fields = ('quantity','product',)
        widgets={
            'product':forms.Select(attrs={'class':'select form-control chosen','data-placeholder':"Selecciona un"}),
        }

class ProductForm(forms.ModelForm):
    def __init__(self,user,*args,**kwargs):
        super (ProductForm,self ).__init__(*args,**kwargs)
        self.fields['menu'].queryset = Menu.objects.filter(company = user.company)
    class Meta:
        model = Product
        fields = ('name','menu','sell_points','units','quantity','image',)
        widgets={
            'menu':forms.Select(attrs={'class':'select form-control chosen',}),
            'units':forms.Select(attrs={'class':'select form-control chosen',}),
            'sell_points':forms.SelectMultiple(attrs={'class':'select form-control chosen','data-placeholder':"Selecciona las sucursales..."}),
            'recipe':forms.SelectMultiple(attrs={'class':'select form-control chosen','data-placeholder':"Selecciona uno o varios productos..."}),
        }

class Product_attrsForm(forms.ModelForm):
    class Meta:
        model = Product_attrs
        fields = ('alias','inventory','price','bar_code','taxes','dynamic_price','primary','active',)
        widgets={
            'taxes':MaterialCheckboxWidget(attrs={'class':'select form-control', 'style':'display:none;'}),
            'dynamic_price':MaterialCheckboxWidget(attrs={'class':'select form-control', 'style':'display:none;'}),
            'primary':MaterialCheckboxWidget(attrs={'class':'select form-control', 'style':'display:none;'}),
            'active':MaterialCheckboxWidget(attrs={'class':'select form-control', 'style':'display:none;'}),
        }

class CuttimeForm(forms.ModelForm):
    class Meta:
        model = Cuttime
        fields = ('time',)
        widgets={
            'time':TimeWidget(attrs={'class':'form-control time-picker', 'placeholder':'Selecciona una fecha...'}),
        }        



