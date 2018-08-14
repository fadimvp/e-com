"""ecommerc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from carts.views import CartView,ItemCountView,CheckoutView,CheckoutFinalView
from orders.views import(
    AddressSelectFormView,
    UserAdressCreateView,
    OrderList,
    OrderDetail
)
from products import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'teams.views.home', name='home'),
    url(r'^form/','teams.views.form',name='form'),
    url(r'^accounts/', include('registration.urls')),
    url(r'^pro/', include('products.urls')),
    url(r'^categories/', include('products.urls_categories')),
    url(r'^cart/$',CartView.as_view(),name='cartt'),
    url(r'^cart/count/$',ItemCountView.as_view(),name='item_count'),
    url(r'^checkout/$',CheckoutView.as_view(),name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$', UserAdressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),
    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
    url(r'^change-language/$',views.change_language,name='change-language'),

]
if settings.DEBUG :
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
