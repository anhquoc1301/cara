from .models import User, TradeUSDT, GuestCheck
import requests
def my_scheduled_job_phase():
    response = requests.get("https://carafinance.com/cron/")

def my_scheduled_job_refresh_guest():
    guests = User.objects.filter(type=3)
    for guest in guests:
        guest_trades=TradeUSDT.objects.filter(user=guest)
        for guest_trade in guest_trades:
            guest_trade.delete()
        guest_check=GuestCheck.objects.get(user=guest)
        guest_check.check_login=True
        guest_check.save()
        guest.wallet=10000
        guest.save()