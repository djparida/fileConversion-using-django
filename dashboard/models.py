from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    product_category = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    shipping_cost = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)


class fileConversion(models.Model):
    myfile = models.FileField(upload_to='myFile/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class convertedFile(models.Model):
    c_file = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)