from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CartItem

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = [ 'quantity']
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': '1', 'value': '1'}),
        }
