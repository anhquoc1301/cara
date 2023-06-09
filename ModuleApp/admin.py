from django.contrib import admin
from .models import Statistic, DataItem, User, TradeUSDT, InputMoney, OutputMoney, BankCardInfo, PhaseUSDT, SetPhaseUSDT, DigitalWalletInfo
# Register your models here.
admin.site.register(Statistic)
admin.site.register(DataItem)
admin.site.register(User)
admin.site.register(TradeUSDT)
admin.site.register(InputMoney)
admin.site.register(OutputMoney)
admin.site.register(BankCardInfo)
admin.site.register(DigitalWalletInfo)
admin.site.register(PhaseUSDT)
admin.site.register(SetPhaseUSDT)