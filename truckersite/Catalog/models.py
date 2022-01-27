from django.db import models
from django.db.models.query_utils import select_related_descend
from django.conf import settings

# Create your models here.

#class categories(models.Model):
 #   word = models.CharField(max_length=50, null=True)
#
    #   def __str__(self):
    #       return self.word

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.TextField(null=True)
    #slug = models.SlugField()
    #description = models.TextField()
    #cat = models.ForeignKey(categories, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.name

class OrderedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.item

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderedProduct)
    startDate = models.DateTimeField(auto_now_add=True)
    orderDate = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
