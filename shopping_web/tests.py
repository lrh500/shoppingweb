from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product,Cart,CartItem

class ProductTests(TestCase):
    def setUp(self):
        self.url = reverse('product_list')


    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


    def test_filter_by_price(self):
        response = self.client.get(self.url, {'price_min': '0', 'price_max': '10'})
        self.assertEqual(response.status_code, 200)


class Cart_addTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lrh5000', password='jsda1234')
        self.client.login(username='lrh5000', password='jsda1234')
        self.product_item = Product.objects.create(producttitle='Puma Men Trek Navy Blue Floater',price=99.99)
        self.url = reverse('cart_detail')

    def test_cart(self):
        response = self.client.post(self.url, {'producttitle': self.product_item.producttitle, 'price': self.product_item.price})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Puma Men Trek Navy Blue Floater')
        

    def test_remove_from_cart(self):
        
        response = self.client.post(self.url, {'product_name': self.product_item.producttitle, 'price': self.product_item.price})
        self.assertEqual(response.status_code, 500)

        
        remove_url = reverse('remove_from_cart')
        response = self.client.post(remove_url, {'product_name': self.product_item.producttitle, 'price': self.product_item.price})
        self.assertEqual(response.status_code, 500)
        self.assertNotContains(response, 'Puma Men Trek Navy Blue Floater')


class RegisterTests(TestCase):
    def setUp(self):
        self.url = reverse('register')

    def new_user_testing(self):
        response = self.client.post(self.url, {
            'username': 'lrh5000',
            'email': 'lrh500@qq.com',
            'password1': 'jsda1234',
            'password2': 'jsda1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def user_testing(self):
        User.objects.create_user(username='lrh5000', password='jsda1234')

        response = self.client.post(self.url, {
            'username': 'lrh5000',
            'email': 'lrh500@qq.com',
            'password1': 'jsda1234',
            'password2': 'jsda1234',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists.')