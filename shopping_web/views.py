from .models import product
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from .forms import RegisterForm, LoginForm
from django.contrib import messages

def index(request):
    try:
        return render(request,'shopping_web/index.html')
    except Exception as e:
        return HttpResponseServerError(e)

def product_list(request):
    try:
        products=product.objects.all()
        return render(request,'shopping_web/product_list.html',{'products':products})
    except Exception as e:
        return HttpResponseServerError(e)

def product_by_name(request,value):
    try:
        product_details=product.objects.filter(producttitle=value)
        return render(request,'shopping_web/product_details.html',{'product_details':product_details})
    except Exception as e:
        return HttpResponseServerError(e)

def register(request):
    try:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('/')
        else:
            form = RegisterForm()
        return render(request, 'shopping_web/register.html', {'form': form})
    except Exception as e:
        return HttpResponseServerError(e)

def user_login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request, request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            form = LoginForm()
        return render(request, 'shopping_web/login.html', {'form': form})
    except Exception as e:
        return HttpResponseServerError(e)

def user_logout(request):
    try:
        logout(request)
        return redirect('/')
    except Exception as e:
        return HttpResponseServerError(e)
