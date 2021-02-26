from django.db import models
from django.contrib.auth.models import User


class fileConversion(models.Model):
    myfile = models.FileField(upload_to='myFile/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class convertedFile(models.Model):
    c_file = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)