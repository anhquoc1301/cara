from .models import Statistic, DataItem, User, InputMoney, OutputMoney, TradeUSDT, PhaseUSDT, SetPhaseUSDT, BankCardInfo, DigitalWalletInfo
from .models import TradeBTC, PhaseBTC, SetPhaseBTC, TradeETH, PhaseETH, SetPhaseETH
from django.http import JsonResponse
from django.db.models import Sum
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random


def my_scheduled_job():
    #get channel websocket
    channel_layer = get_channel_layer()

    # result last phase
    lastPhase = PhaseUSDT.objects.latest('create_at')
    trades = TradeUSDT.objects.filter(phase=lastPhase)
    resultPhase = lastPhase.a+lastPhase.c+lastPhase.c
    for trade in trades:
        if resultPhase >= 13 and trade.type_choice == 1:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*1.96
        elif resultPhase <= 13 and trade.type_choice == 2:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*1.96
        elif resultPhase % 2 == 1 and trade.type_choice == 3:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*1.96
        elif resultPhase % 2 == 0 and trade.type_choice == 4:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*1.96
        elif resultPhase >= 13 and resultPhase % 2 == 1 and trade.type_choice == 5:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*3.96
        elif resultPhase <= 13 and resultPhase % 2 == 1 and trade.type_choice == 6:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*3.96
        elif resultPhase >= 13 and resultPhase % 2 == 0 and trade.type_choice == 7:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*3.96
        elif resultPhase <= 13 and resultPhase % 2 == 0 and trade.type_choice == 8:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*3.96
        elif resultPhase == 27 and trade.type_choice == 9:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*15
        elif resultPhase == 0 and trade.type_choice == 10:
            trade.result = 1
            trade.trade_value_win = trade.trade_value*15
        else:
            trade.result=2
        trade.save()
        user=User.objects.get(id=trade.user.id)
        if trade.result==1:
            user.wallet+=trade.trade_value_win
            user.save()
            message = {
                "result": "win",
                "wallet": user.wallet,
                "trade_id": trade.id,
                "trade_value": trade.trade_value,
                "trade_value_win": trade.trade_value_win,
                "a": lastPhase.a,
                "b": lastPhase.b,
                "c": lastPhase.c,
            }
            async_to_sync(channel_layer.group_send)(
                user.username,
                {
                    "type": "chat_message",
                    "message": message
                },
            )

        elif trade.result==2:
            message = {
                "result": "lose",
                "trade_id": trade.id,
                "trade_value": trade.trade_value,
                "a": lastPhase.a,
                "b": lastPhase.b,
                "c": lastPhase.c,
            }
            async_to_sync(channel_layer.group_send)(
                user.username,
                {
                    "type": "chat_message",
                    "message": message
                },
            )

    # create phase
    new_phase = PhaseUSDT.objects.create(code=random.randint(0000000, 9999999))
    set_phase = SetPhaseUSDT.objects.first()
    if set_phase.a == -1 or set_phase.b == -1 or set_phase.c == -1:
        had_set = False
    else:
        had_set = True
    new_phase.input_phase(a=set_phase.a, b=set_phase.b,
                          c=set_phase.c, had_set=had_set)
    set_phase.refresh_phase_set()

    message = {
        "time": new_phase.create_at,
        "code": new_phase.code,
        "a": new_phase.a,
        "b": new_phase.b,
        "c": new_phase.c
    }
    async_to_sync(channel_layer.group_send)(
        'normal',
        {
            "type": "chat_message",
            "message": message
        },
    )
