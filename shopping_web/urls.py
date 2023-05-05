from django.urls import path
from . import views

urlpatterns = [
path('',views.index,name='index'),
path('product_list', views.product_list, name='product_list'),
path('product_details/<str:value>/', views.product_by_name,name='product_by_name'),
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
]