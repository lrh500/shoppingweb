from .models import Product,Cart,CartItem
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseServerError
from django.views.decorators.http import require_POST
from .forms import RegisterForm, LoginForm,CartItemForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import pandas as pd
import matplotlib.pyplot as plt
import mpld3



def index(request):
    try:
        return render(request,'shopping_web/index.html')
    except Exception as e:
        return HttpResponseServerError(e)

def product_list(request):
    try:
        gender = request.GET.get('gender', '')
        category = request.GET.get('category', '')
        sub_category = request.GET.get('sub_category', '')
        product_type = request.GET.get('product_type', '')
        colour = request.GET.get('colour', '')
        usage = request.GET.get('usage', '')

        query = Q()
        if gender:
            query &= Q(gender=gender)
        if category:
            query &= Q(category=category)
        if sub_category:
            query &= Q(subCategory=sub_category)
        if product_type:
            query &= Q(productType=product_type)
        if colour:
            query &= Q(colour=colour)
        if usage:
            query &= Q(usage=usage)

        search_query = request.GET.get('q', '')
        if search_query:
            product_details = Product.objects.filter(
                Q(producttitle__icontains=search_query) | Q(category__icontains=search_query) |
                Q(subCategory__icontains=search_query) | Q(productType__icontains=search_query) |
                Q(colour__icontains=search_query) | Q(usage__icontains=search_query)
            ).filter(query)
        else:
            product_details = Product.objects.filter(query)

        return render(request, 'shopping_web/product_list.html', {'product_details': product_details})
    except Exception as e:
        return HttpResponseServerError(e)



def product_by_name(request,product_id):
    try:
        product_details=Product.objects.filter(productId=product_id)
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
                return redirect('register_success')
            else:
                return redirect('error')
        else:
            form = RegisterForm()
        return render(request, 'shopping_web/register.html', {'form': form, 'message': 'Registration failed. Please try again.'})
    except Exception as e:
        return HttpResponseServerError(e)

def register_success(request):
    return render(request, 'shopping_web/register_success.html')
def register_fail(request):
    return render(request, 'shopping_web/error.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
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
        form = LoginForm()
        return render(request, 'shopping_web/login.html', {'form': form})
    except Exception as e:
        return HttpResponseServerError(e)

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        return render(request, 'shopping_web/cart_detail.html', {'cart': cart, 'cart_items': cart_items})
    except Exception as e:
        return HttpResponseServerError(e)

def cart_add(request, product_id):
    try:
        if not request.user.is_authenticated:           
            return redirect('login')
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, productId=product_id)
        form = CartItemForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart_item = None
            cart_items = CartItem.objects.filter(cart=cart, product=product)
            if cart_items.exists():
                cart_item = cart_items.first()
                cart_item.quantity += cd['quantity']
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=cd['quantity'],
                    price=product.price
                )
            return redirect('cart_detail')
        else:
            
            context = {'product': product, 'form': form}
            return render(request, 'shopping_web/cart_add.html', context)
    except Exception as e:
        return HttpResponseServerError(e)





def cart_remove(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, productId=product_id)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart_detail')

def clear_cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items.delete()
        return redirect('cart_detail')
    except Cart.DoesNotExist:
        return redirect('cart_detail')

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total_price = cart.total_price
    return render(request,'shopping_web/checkout.html')


def compare(request):
    if request.method == 'POST':
        products1 = request.POST.get('products')
        products2 = request.POST.get('products2')

        if not products1 or not products2:
            messages.error(request, 'Please select 2 products to compare.')
            return redirect('compare')

        data = {
            products1: list(Product.objects.filter(producttitle=products1).values_list('price', flat=True)),
            products2: list(Product.objects.filter(producttitle=products2).values_list('price', flat=True))
        }

        df = pd.DataFrame(data)

        ax = df.plot(kind='bar', rot=0, figsize=(10, 6))
        ax.set_xlabel('Product')
        ax.set_ylabel('Price')
        ax.set_title('Comparison of selected products')
        ax.set_xticks(range(len(df.columns)))
        ax.set_xticklabels(df.columns)

        html = mpld3.fig_to_html(ax.figure)
        products = Product.objects.values_list('producttitle', flat=True)
        return render(request, 'shopping_web/compare.html', {'html': html, 'products': products})

    else:
        products = Product.objects.values_list('producttitle', flat=True)
        return render(request, 'shopping_web/compare.html', {'products': products})





