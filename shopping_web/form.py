from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User



