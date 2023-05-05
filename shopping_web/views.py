from .models import Product,Cart,CartItem
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseServerError
from django.views.decorators.http import require_POST
from .forms import RegisterForm, LoginForm,CartItemForm
from django.contrib import messages

def index(request):
    try:
        return render(request,'shopping_web/index.html')
    except Exception as e:
        return HttpResponseServerError(e)

def product_list(request):
    try:
        products=Product.objects.all()
        return render(request,'shopping_web/product_list.html',{'products':products})
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


def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        return render(request, 'shopping_web/cart_detail.html', {'cart': cart, 'cart_items': cart_items})
    except Exception as e:
        return HttpResponseServerError(e)


def cart_add(request, product_id):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    product = get_object_or_404(Product, productId=product_id)
    form = CartItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=cd['quantity'],
            price=product.price
        )
        return redirect('cart_detail')
    else:
        # Handle the case where the form is not valid
        # You can add an error message to the context and render the template again
        context = {'product': product, 'form': form}
        return render(request, 'shopping_web/cart_add.html', context)

def cart_remove(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, productId=product_id)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart_detail')

#def cart_detail(request):
#    cart = Cart.objects.get(user=request.user)
#    cart_items = cart.items.all()
#    return render(request, 'shopping_web/cart_detail.html', {'cart': cart, 'cart_items': cart_items})
