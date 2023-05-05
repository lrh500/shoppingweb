from django.urls import path
from . import views

urlpatterns = [
path('',views.index,name='index'),
path('product_list/', views.product_list, name='product_list'),
path('product_details/<int:product_id>/', views.product_by_name,name='product_by_name'),
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('register_success',views.register_success,name='register_success'),
path('error',views.register_fail,name='error'),
path('cart_detail/', views.cart_detail, name='cart_detail'),
path('cart_add/<int:product_id>/', views.cart_add, name='cart_add'),
path('cart_remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]