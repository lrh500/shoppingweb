from .models import product
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
# Create your views here.

def index(request):
    return render(request,'shopping_web/index.html')


def product_list(request):
    products=product.objects.all()
    return render(request,'shopping_web/product_list.html',{'products':products})

def product_by_name(request,value):
    product_details=product.objects.filter(producttitle=value)
    return render(request,'shopping_web/product_details.html',{'product_details':product_details})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')