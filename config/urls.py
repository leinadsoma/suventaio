from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from project.app.views import *

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', index, name='index'),

    url(r'^invoice/$', invoice, name='invoice'),
    url(r'^select-sellpoint/$', select_sellpoint, name='select_sellpoint'),

    url(r'^users/$', users, name='users'),
    url(r'^user/(.+)/$', user_form, name='user_form'),
    url(r'^change-password/(.+)/$', change_password, name='change_password'),

    url(r'^sellpoints/$', sellpoints, name='sellpoints'),
    url(r'^sellpoint/(.+)/$', sellpoint_form, name='sellpoint_form'),

    url(r'^menus/$', menus, name='menus'),
    url(r'^menu/(.+)/$', menu_form, name='menu_form'),
    url(r'^menus_ajax/$', menus_ajax, name='menus_ajax'),

    url(r'^products/$', products, name='products'),
    url(r'^product/(.+)/$', product_form, name='product_form'),
    url(r'^product-attributes/(.+)/$', product_attributes, name='product_attributes'),
    url(r'^product-attribute/$', product_attribute_form, name='product_attribute_form'),

    url(r'^recipes/(.+)/$', recipes, name='recipes'),
    url(r'^recipe/(.+)/$', recipe_form, name='recipe_form'),

    url(r'^vendor/(.+)/$', vendor, name='vendor'),

    url(r'^sellpoints-cut/$', sellpoints_cut, name='sellpoints_cut'),
    url(r'^cut-times/(.+)/$', cut_times, name='cut_times'),
    url(r'^cut-time/(.+)/$', cut_time_form, name='cut_time_form'),
    url(r'^cuts/(.+)/$', cuts, name='cuts'),
    url(r'^cut-details/$', cut_details, name='cut_details'),

    url(r'^ticket-detail/(.+)/$', ticket_detail, name='ticket_detail'),

    url(r'^user_logout/$', user_logout, name='user_logout'),
    url(r'^login/$', user_login, name='user_login'),
    url(r'^privacity/$', privacity, name='privacity'),

    url(r'^invoice-sellpoint/$', invoice_sellpoint, name='invoice_sellpoint'),
    url(r'^invoice-sellpoint/(.+)/$', invoice_sellpoint_form, name='invoice_sellpoint_form'),

    ###FINEZIPO
    url(r'^finezipo/nosotros/$', finezipo_nosotros, name='finezipo_nosotros'),
    url(r'^finezipo/artistas/(.+)/$', finezipo_artistas, name='finezipo_artistas'),
    url(r'^finezipo/contacto/$', finezipo_contacto, name='finezipo_contacto'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


