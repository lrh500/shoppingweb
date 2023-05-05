from django.shortcuts import render
from .models import product
# Create your views here.

def index(request):
    return render(request,'shopping_web/index.html')


def product_list(request):
    products=product.objects.all()
    return render(request,'shopping_web/product_list.html',{'products':products})