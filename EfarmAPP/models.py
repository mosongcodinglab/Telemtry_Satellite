from django.db import models

# Create your models here.
class fields(models.Model):
    _id = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    name = models.CharField(max_length=90)
    area= models.FloatField(max_length=60)
    gps= models.FloatField (max_length=200)
    note=models.CharField(max_length=150)
    createdAt=models.DateField
    