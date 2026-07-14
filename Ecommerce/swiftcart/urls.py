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
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("wishlist/", views.wishlist, name="wishlist"),

path(
    "add-to-wishlist/<int:product_id>/",
    views.add_to_wishlist,
    name="add_to_wishlist"
),

path(
    "remove-from-wishlist/<int:product_id>/",
    views.remove_from_wishlist,
    name="remove_from_wishlist"
),
path(
    'checkout/',
    views.checkout,
    name='checkout'
),
path("place-order/", views.place_order, name="place_order"),
path(
    "order-success/",
    views.order_success,
    name="order_success"
),
path(
    "wishlist/toggle/<int:product_id>/",
    views.toggle_wishlist,
    name="toggle_wishlist"
),
path(
    "cart/ajax-add/<int:product_id>/",
    views.ajax_add_to_cart,
    name="ajax_add_to_cart"
),
# ================= STATIC PAGES =================

path("privacy/", views.privacy, name="privacy"),

path("refund/", views.refund, name="refund"),

path("shipping/", views.shipping, name="shipping"),

path("terms/", views.terms, name="terms"),

path("mission/", views.mission, name="mission"),

path("vision/", views.vision, name="vision"),
path("profile/", views.profile, name="profile"),

path("profile/edit/", views.edit_profile, name="edit_profile"),
]