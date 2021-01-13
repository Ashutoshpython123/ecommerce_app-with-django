"""ecommerce_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . views import (
    HomeView,
    ProductDetailView,
    add_to_cart,
    Order_Summary,
    remove_from_cart,
    remove_single_item_from_cart

)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name="Home"),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('order-summary/', Order_Summary, name='order-summary'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),

    path("register/", views.register, name= "register"),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name="logout")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
