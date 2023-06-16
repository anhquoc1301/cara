from django.db import models

# Create your models here.

class test(models.Model):
    value=models.CharField(max_length=10)
    