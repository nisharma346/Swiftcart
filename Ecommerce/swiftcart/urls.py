from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/', views.category_list, name='category'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact_us, name='contact'),
]