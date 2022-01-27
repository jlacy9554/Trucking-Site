from django.db import models
from django.conf import settings


class Uregister(models.Model):
    Name  = models.CharField( max_length=50)
    lname = models.CharField( max_length=50)
    PhoneNo = models.CharField(max_length=12)
    Email = models.EmailField( max_length=254)
    Address = models.CharField( max_length=50)
    address2 = models.CharField( max_length=50)
    city = models.CharField( max_length=50)
    state = models.CharField( max_length=50)
    zipcode = models.CharField( max_length=50)
    org = models.CharField( max_length=50)
    sponsor = models.CharField( max_length=50)
    class Meta:
        db_table="USER"
        db_table="DRIVER"
        db_table= "DRIVER_ADDRESS"