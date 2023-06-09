from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    code=models.IntegerField(null=True)
    referrer=models.IntegerField(null=True)
    level_choice = ((0, 'Level 0'),(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'),(4, 'Level 4'), (5, 'Level 5'))
    level=models.IntegerField(choices=level_choice, default=0)
    bonus=models.FloatField(default=0)
    coin=models.IntegerField(null=True)
    total_deal=models.IntegerField(null=True)
    bonuscoin=models.FloatField(null=True)
    referrer_temporary=models.IntegerField(null=True)



class BetDeal(models.Model):
    create_at=models.DateTimeField(auto_now_add=True)
    coin_deal=models.IntegerField(null=False)
    user=models.IntegerField(null=False)
    def __str__(self):
        return self.user



class Deal(models.Model):
    create_at=models.DateTimeField(auto_now_add=True)
    coin_deal=models.IntegerField(null=False)
    unto=models.IntegerField(null=False)
    user=models.IntegerField(null=False)
    def __str__(self):
        return self.user


class InputCoin(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    coin_deal = models.IntegerField(null=False)
    user=models.IntegerField(null=False)
    def __str__(self):
        return self.user

class OutputCoin(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    coin_deal = models.IntegerField(null=False)
    user=models.IntegerField(null=False)
    def __str__(self):
        return self.user