from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class product(models.Model):
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

    def __str__(self):
        return f'{self.productId}, {self.gender}, {self.category},{self.subCategory},{self.productType},{self.colour},{self.usage},{self.producttitle},{self.image},{self.imageURL}'

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.user.username} ordered {self.quantity} of {self.product.producttitle}'
