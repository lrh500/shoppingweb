from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product,Order
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)

# Define a new UserAdmin class
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_superuser')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)