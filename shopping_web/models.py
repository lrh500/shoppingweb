from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    productId=models.IntegerField(primary_key=True)
    gender=models.TextField()
    category=models.TextField()
    subCategory=models.TextField()
    productType=models.TextField()
    colour=models.TextField()
    usage=models.TextField()
    producttitle=models.TextField()
    image=models.ImageField()
    imageURL=models.TextField()
    price=models.FloatField()

    def __str__(self):
        return f'{self.productId}, {self.gender}, {self.category},{self.subCategory},{self.productType},{self.colour},{self.usage},{self.producttitle},{self.image},{self.imageURL},{self.price}'

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.user.username} ordered {self.quantity} of {self.Product.producttitle}'


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.producttitle}'

    @property
    def total_price(self):
        return self.price * self.quantity

    def get_absolute_url(self):
        return reverse('product_by_name', args=[self.product.producttitle])