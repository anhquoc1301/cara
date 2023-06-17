from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, DataItem, User, InputMoney, OutputMoney, GuestCheck
from .models import TradeUSDT, PhaseUSDT, SetPhaseUSDT, BankCardInfo, DigitalWalletInfo
from faker import Faker
from django.http import JsonResponse
from django.db.models import Sum
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from MultiLevelApp.decorators import admin_only, staff_only
import random
import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
# Create your views here.

def main(request):
    today = datetime.datetime.today()
    # users=User.objects.all().order_by('-create_at')[1:6]
    # a=User.objects.earliest('create_at')
    us=User.objects.get(username='anh1301')
    
    today = datetime.date.today()
    print(today)
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=200)
    print(last_month)
    if request.method == 'POST':
        
        print(request.POST.get("username"))
    return render(request, 'home/admindashboard.html')

# def main(request):
#     qs= Statistic.objects.all()
#     if request.method=="POST":
#         new_stat = request.POST.get('new-statistic')
#         obj , _ =Statistic.objects.get_or_create(name=new_stat)
#         return redirect("stats:dashboard", obj.slug)
#     return render(request, 'main.html', {'qs': qs})

def dashboard(request, slug):
    print("check")
    obj = get_object_or_404(Statistic, slug=slug)
    return render(request, 'dashboard.html',{
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data,
        'user': request.user.username if request.user.username else fake.name()
    })

def chart_data(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    qs = obj.data.values('owner').annotate(Sum('value'))
    chart_data = [x['value__sum'] for x in qs]
    chart_labels= [x['owner'] for x in qs]
    return JsonResponse({
        'chartData': chart_data,
        'chartLabels': chart_labels
    })

class register(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'TradeBTC/signup.html')
        else:
            return redirect('app:home')
    def post(self, request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            password2=request.POST.get('password2')
            code=random.randint(1000000, 9999999)
            while User.objects.filter(code=code).exists():
                code = random.randint(1000000, 9999999)
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Tên đăng nhập trùng!')
                return redirect('app:register')
            if password==password2:
                user=User.objects.create_user(username=username, password=password, email=None)
                user.code=code
                user.save()
                messages.success(request, 'Đăng ký thành công!')
                return redirect('app:login')
            else:
                messages.warning(request, 'Mật khẩu không khớp!')
                return redirect('app:register')
            
class login(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'TradeBTC/login.html')
        else:
            return redirect('app:home')
    def post(self,request):
        username = request.POST.get('username')
        password= request.POST.get('password')
        myUser = authenticate(request, username=username, password=password)
        if myUser is None:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu!')
            return redirect('app:login')
        auth.login(request, myUser)
        if myUser.type==0:
            return redirect('app:home')
        elif myUser.type==1:
            return redirect('app:list_accept_input_money')
        elif myUser.type==2:
            return redirect('app:home')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('app:login')

@login_required
def home(request):
    user=request.user.wallet
    return render(request, 'TradeBTC/index.html', {'user': user})

@login_required
def service(request):
    return render(request, 'TradeBTC/servicecustomer.html')

@login_required
def change_password(request):
    user=User.objects.get(id=request.user.id)
    if request.method=="POST":
        password=request.POST['password']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2 and user.check_password(password):
                user.set_password(password2)
                user.save()
                messages.success(request, 'Đổi mật khẩu thành công!')
                user_response=authenticate(username=user.username, password=password2)
                auth.login(request, user_response)
                return redirect('app:home')
        else:
            messages.warning('Mật khẩu không khớp!')
            return redirect('app:change_password')
    return render(request, 'TradeBTC/changepassword.html')

@login_required
def edit_password_wallet(request):
    user=User.objects.get(id=request.user.id)
    if user.wallet_password is not None:
        if request.method=="POST":
            password=request.POST['password']
            password1=request.POST['password1']
            password2=request.POST['password2']
            if password1==password2 and user.wallet_password==password:
                    user.wallet_password=password2
                    user.save()
                    messages.success(request, 'Đổi mật khẩu thành công!')
                    return redirect('app:dashboard')
            else:
                messages.warning('Mật khẩu không khớp!')
                return redirect('app:edit_password_wallet')
        return render(request, 'TradeBTC/changepasswithdrawmoney2.html')
    else:
        if request.method=="POST":
            password1=request.POST['password1']
            password2=request.POST['password2']
            if password1==password2:
                    user.wallet_password=password2
                    user.save()
                    messages.success(request, 'Đổi mật khẩu thành công!')
                    return redirect('app:dashboard')
            else:
                messages.warning('Mật khẩu không khớp!')
                return redirect('app:edit_password_wallet')
        return render(request, 'TradeBTC/changepasswithdrawmoney1.html')

@login_required
def dashboard(request):
    user=User.objects.get(id=request.user.id)
    return render(request, 'TradeBTC/dashboard.html', {'user': user})

@login_required
def wallet(request):
    user=User.objects.get(id=request.user.id)
    bankCard=BankCardInfo.objects.filter(user=user)
    digitalWallet=DigitalWalletInfo.objects.filter(user=user)
    context={
        'user': user,
        'bank': bankCard,
        'digital':digitalWallet,
    }
    return render(request, 'TradeBTC/mywallet.html', context)

@login_required
def add_method(request):
    user=User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            bank_name = request.POST['bank_name']
            bank_account = request.POST['bank_account']
            bank_opening_address = request.POST['bank_opening_address']
            user_name = request.POST['user_name']
            bank_number = request.POST['bank_number']
            bank_cvv = request.POST['bank_cvv']
            bank_password = request.POST['bank_password']
            BankCardInfo.objects.create(user=user, 
                                        bank_name=bank_name, 
                                        bank_account=bank_account, 
                                        bank_opening_address=bank_opening_address, 
                                        user_name=user_name, bank_number=bank_number, 
                                        bank_cvv=bank_cvv, 
                                        bank_password=bank_password)
            return redirect('app:wallet')
        elif request.POST.get("form_type") == 'formTwo':
            user_name = request.POST['user_name']
            wallet_number = request.POST['wallet_number']
            DigitalWalletInfo.objects.create(user_name=user_name, 
                                             wallet_number=wallet_number, 
                                             user=user)
            return redirect('app:wallet')
    return render(request, 'TradeBTC/addmethod.html')

@login_required
def input_money(request):
    if request.method=="POST":
        value=int(request.POST.get('value'))
        user=User.objects.get(id=request.user.id)
        InputMoney.objects.create(value=value, user=user)
        messages.success(request, 'Tạo lệnh rút tiền thành công!')
        return redirect('app:input_money')
    return render(request, 'TradeBTC/recharge.html')

@login_required
def output_money(request):
    user=User.objects.get(id=request.user.id)
    bankCard=BankCardInfo.objects.filter(user=user)
    digitalWallet=DigitalWalletInfo.objects.filter(user=user)
    context={
        'user': user,
        'bank': bankCard,
        'digital':digitalWallet,
    }
    if request.method=="POST":
        value=int(request.POST.get('value'))
        password=request.POST.get('password')
        if user.wallet>=value and user.wallet_password==password:
            outputMoney=OutputMoney.objects.create(value=value, user=user)
            outputMoney.save()
            messages.success(request, 'Tạo lệnh rút tiền thành công!')
            return redirect('app:output_money')
        else:
            messages.warning(request, 'Rút tiền thất bại!')
            return redirect('app:output_money')
    return render(request, 'TradeBTC/outputmoney.html', context)

@login_required
def history_output(request):
    data=OutputMoney.objects.filter(user=request.user)
    context={'data': data}
    return render(request, 'TradeBTC/historyoutput.html', context)

@login_required
def history_input(request):
    data=InputMoney.objects.filter(user=request.user)
    context={'data': data}
    return render(request, 'TradeBTC/historyinput.html', context)

@login_required
def history_trade(request):
    data=Trade.objects.filter(user=request.user)
    context={'data': data}
    return render(request, 'history_trade.html', context)

#Just ADMIN
@admin_only
@login_required
def list_accept_input_money(request):
    inputMoney=InputMoney.objects.filter(status='Pending')
    print(inputMoney.count())
    context={'data': inputMoney}
    return render(request, 'home/listacceptinputmoney.html', context)

@login_required
@admin_only
def accept_input_money(request, pk):
    inputMoney=InputMoney.objects.get(id=pk)
    context={'data': inputMoney}
    if request.method == 'POST':
        detail = request.POST['detail']
        valueControl = int(request.POST['value_control'])
        valueReal = int(request.POST['value_real'])
        inputMoney.value_control=valueControl
        inputMoney.value_real=valueReal
        inputMoney.detail=detail
        inputMoney.status='Success'
        inputMoney.save()
        user=User.objects.get(id=inputMoney.user.id)
        user.wallet+=inputMoney.value_real
        user.save()
        messages.success(request, 'Thành công!')
        return redirect('app:list_accept_input_money')
    return render(request, 'acceptinputmoney.html', context)

@login_required
@admin_only
def cancel_status_input_money(request, pk):
    inputMoney=InputMoney.objects.get(id=pk)
    inputMoney.status='Fail'
    inputMoney.save()
    messages.success(request, 'Thành công!')
    return redirect('app:list_accept_input_money')

@login_required
@admin_only
def list_accept_output_money(request):
    outputMoney=OutputMoney.objects.filter(status='Pending')
    context={'data': outputMoney}
    return render(request, 'home/listacceptoutputmoney.html', context)

@login_required
@admin_only
def accept_status_output_money(request, pk):
    outputMoney=OutputMoney.objects.get(id=pk)
    user=User.objects.get(id=outputMoney.user.id)
    if user.wallet>=outputMoney.value:
        outputMoney.status='Success'
        outputMoney.save()
        user.wallet-=outputMoney.value
        user.save()
        messages.success(request, 'Thành công!')
        return redirect('app:list_accept_output_money')
    else:
        outputMoney.status='Fail'
        outputMoney.save()
        messages.warning(request, 'Thất bại!')
        return redirect('app:list_accept_output_money')

@login_required
@admin_only
def cancel_status_output_money(request, pk):
    outputMoney=OutputMoney.objects.get(id=pk)
    outputMoney.status='Fail'
    outputMoney.save()
    messages.success(request, 'Thành công!')
    return redirect('app:list_accept_output_money')

@login_required
@admin_only
def list_staff(request):
    staffs=User.objects.filter(type=2)
    context={'data': staffs}
    return render(request, 'home/liststaff.html', context)

@login_required
@admin_only
def detail_staff(request, pk):
    staff=User.objects.get(id=pk)
    users=User.objects.filter(referrer=staff.code)
    outputs_month = []
    inputs_month = []
    today = datetime.datetime.today()
    for user in users:
        output_money_month = OutputMoney.objects.filter(user=user).filter(timestamp__year=today.year).filter(timestamp__month=today.month).filter(status='Success')
        input_money_month = InputMoney.objects.filter(user=user).filter(timestamp__year=today.year).filter(timestamp__month=today.month).filter(status='Success')
        outputs_month.append(output_money_month)
        inputs_month.append(input_money_month)
    input_month_value = 0
    output_month_value = 0
    for i in outputs_month:
        output_month_value+=i.value
    for i in inputs_month:
        input_month_value+=i.value_control
    revenue = input_month_value-output_month_value
    if revenue>9999:
        basic_salary=1100
    else:
        basic_salary=855
    if 0<revenue<10000:
        total_salary=basic_salary+revenue*0.05
    elif 10000 <= revenue < 40000:
        total_salary=basic_salary+revenue*0.07
    elif 40000 <= revenue < 70000:
        total_salary=basic_salary+revenue*0.09
    elif 70000<=revenue<100000:
        total_salary=basic_salary+revenue*0.11
    elif 100000<=revenue<130000:
        total_salary=basic_salary+revenue*0.13
    elif 130000<=revenue:
        total_salary=basic_salary+revenue*0.15
    else:
        total_salary=basic_salary
    context={
        'output_month_value': output_month_value,
        'input_month_value': input_month_value,
        'basic_salary': basic_salary,
        'total_salary': total_salary,
        'total_user': users.count()
    }
    
    return render(request, 'home/detailstaff.html', context)

@login_required
@admin_only
def detail_staff_last_month(request, pk):
    staff=User.objects.get(id=pk)
    users=User.objects.filter(referrer=staff.code)
    outputs_month = []
    inputs_month = []
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=40)
    for user in users:
        output_money_month = OutputMoney.objects.filter(user=user).filter(timestamp__year=last_month.year).filter(timestamp__month=last_month.month).filter(status='Success')
        input_money_month = InputMoney.objects.filter(user=user).filter(timestamp__year=last_month.year).filter(timestamp__month=last_month.month).filter(status='Success')
        outputs_month.append(output_money_month)
        inputs_month.append(input_money_month)
    input_month_value = 0
    output_month_value = 0
    for i in outputs_month:
        output_month_value+=i.value
    for i in inputs_month:
        input_month_value+=i.value_control
    revenue = input_month_value-output_month_value
    if revenue>9999:
        basic_salary=1100
    else:
        basic_salary=855
    if 0<revenue<10000:
        total_salary=basic_salary+revenue*0.05
    elif 10000 <= revenue < 40000:
        total_salary=basic_salary+revenue*0.07
    elif 40000 <= revenue < 70000:
        total_salary=basic_salary+revenue*0.09
    elif 70000<=revenue<100000:
        total_salary=basic_salary+revenue*0.11
    elif 100000<=revenue<130000:
        total_salary=basic_salary+revenue*0.13
    elif 130000<=revenue:
        total_salary=basic_salary+revenue*0.15
    else:
        total_salary=basic_salary
    context={
        'output_month_value': output_month_value,
        'input_month_value': input_month_value,
        'basic_salary': basic_salary,
        'total_salary': total_salary,
    }
    
    return render(request, 'home/detailstafflastmonth.html', context)

@login_required
@admin_only
def add_staff(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        code=random.randint(1000000, 9999999)
        while User.objects.filter(code=code).exists():
            code = random.randint(1000000, 9999999)
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Tên đăng nhập trùng!')
            return redirect('app:add_staff')
        user=User.objects.create_user(username=username, password=password, type=2, email=None, code=code)
        user.save()
        messages.success(request, 'Đăng ký thành công!')
        return redirect('app:list_staff')
    return render(request, 'home/addstaff.html')

@login_required
@admin_only
def list_user(request):
    users=User.objects.filter(type=0)
    context={'data': users}
    return render(request, 'home/listuser.html', context)

@login_required
@admin_only
def list_user_not_referrer(request):
    users=User.objects.filter(type=0, referrer=None)
    context={'data': users}
    return render(request, 'home/listusernotreferrer.html', context)

@login_required
@admin_only
def set_user_referrer(request, pk):
    user=User.objects.get(id=pk)
    if request.method == 'POST':
        referrer = int(request.POST['referrer'])
        user.referrer=referrer
        user.save()
        messages.success(request, 'Thành công!')
        return redirect('app:list_user_not_referrer')
    context={'data': user}
    return render(request, 'home/setreferrer.html', context)

@login_required
@admin_only
def admin_dashboard(request):
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=40)
    last_last_month = first - datetime.timedelta(days=70)
    output_money_month = OutputMoney.objects.filter(timestamp__year=today.year).filter(timestamp__month=today.month).filter(status='Success')
    input_money_month = InputMoney.objects.filter(timestamp__year=today.year).filter(timestamp__month=today.month).filter(status='Success')
    output_money_last_month = OutputMoney.objects.filter(timestamp__year=last_month.year).filter(timestamp__month=last_month.month).filter(status='Success')
    input_money_last_month = InputMoney.objects.filter(timestamp__year=last_month.year).filter(timestamp__month=last_month.month).filter(status='Success')
    output_money_last_last_month = OutputMoney.objects.filter(timestamp__year=last_last_month.year).filter(timestamp__month=last_last_month.month).filter(status='Success')
    input_money_last_last_month = InputMoney.objects.filter(timestamp__year=last_last_month.year).filter(timestamp__month=last_last_month.month).filter(status='Success')
    output_month_value = 0
    input_month_value = 0
    output_last_month_value = 0
    input_last_month_value = 0
    output_last_last_month_value = 0
    input_last_last_month_value = 0
    for i in output_money_month:
        output_month_value+=i.value
    for i in input_money_month:
        input_month_value+=i.value_control
    for i in output_money_last_month:
        output_last_month_value+=i.value
    for i in input_money_last_month:
        input_last_month_value+=i.value_control
    for i in output_money_last_last_month:
        output_last_last_month_value+=i.value
    for i in input_money_last_last_month:
        input_last_last_month_value+=i.value_control
    context={
        'output_month_value': output_month_value,
        'input_month_value': input_month_value,
        'output_last_month_value': output_last_month_value,
        'input_last_month_value': input_last_month_value,
        'output_last_last_month_value': output_last_last_month_value,
        'input_last_last_month_value': input_last_last_month_value
        }
    return render(request, 'home/admindashboard.html', context)


#Just Staff
@login_required
@staff_only
def staff_dashboard(request):
    staff = request.user
    users=User.objects.filter(referrer=staff.code)
    outputs = []
    inputs = []
    outputs_month = []
    inputs_month = []
    today = datetime.datetime.today()
    for user in users:
        output_money = OutputMoney.objects.filter(user=user)
        input_money = InputMoney.objects.filter(user=user)
        outputs.append(output_money)
        inputs.append(input_money)
        output_money_month = OutputMoney.objects.filter(timestamp__year=today.year).filter(timestamp__month=today.month)
        input_money_month = InputMoney.objects.filter(timestamp__year=today.year).filter(timestamp__month=today.month)
        outputs_month.append(output_money_month)
        inputs_month.append(input_money_month)
    
    return redirect('app:list_accept_output_money')


@login_required
def invest(request):
    channel_layer = get_channel_layer()

    user=User.objects.get(id=request.user.id)
    phase = PhaseUSDT.objects.latest('create_at')
    today = datetime.datetime.today()
    last_phases= PhaseUSDT.objects.all().order_by('-create_at')[1:6]
    try:
        trades=TradeUSDT.objects.filter(user=user).filter(create_at__year=today.year).filter(create_at__month=today.month).filter(create_at__day=today.day)
    except:
        trades = None
    trade_all_value=0
    for trade in trades:
        trade_all_value+=trade.trade_value
    
    if request.method == 'POST':
        value=int(request.POST.get('value', None))
        type=int(request.POST.get('type', None ))
        if user.wallet>=value:
            trade = TradeUSDT.objects.create(trade_value=value, trade_type=type, phase=phase, user=user)
            user.wallet-=value
            user.save()
            trade_all_value_new=trade_all_value+value
            message = {
                "wallet": str(user.wallet),
                "trade": str(trade),
                "trade_all_value": str(trade_all_value_new),
            }
            print(user.username)
            async_to_sync(channel_layer.group_send)(
                user.username,
                {
                    "type": "chat_message",
                    "message": message
                },
            )
            message = {
                "trade_value_client": str(trade.trade_value),
                "trade_type_client": str(trade.trade_type)
            }
            async_to_sync(channel_layer.group_send)(
                "normal",
                {
                    "type": "chat_message",
                    "message": message
                },
            )
        else:
            messages.warning(request, 'Fail !')
    context = {
        "user": user,
        'phase': phase,
        "last_phases": last_phases,
        'trades': trades,
        'trade_all_value':trade_all_value
        
    }
    return render(request, 'TradeBTC/invest.html', context )

def cron(request):
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
                "wallet": str(user.wallet),
                "trade_id": str(trade.id),
                "trade_value": str(trade.trade_value),
                "trade_value_win": str(trade.trade_value_win),
                "a": str(lastPhase.a),
                "b": str(lastPhase.b),
                "c": str(lastPhase.c),
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
                "trade_id": str(trade.id),
                "trade_value": str(trade.trade_value),
                "a": str(lastPhase.a),
                "b": str(lastPhase.b),
                "c": str(lastPhase.c),
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
        "time": str(new_phase.create_at),
        "code": str(new_phase.code),
        "a": str(new_phase.a),
        "b": str(new_phase.b),
        "c": str(new_phase.c)
    }
    async_to_sync(channel_layer.group_send)(
        'normal',
        {
            "type": "chat_message",
            "message": message
        },
    )
    return HttpResponse('chiehfhj,sdfe')

def guest_login(request):
    guests=User.objects.filter(type=3)
    for i in guests:
        check=GuestCheck.objects.get(user=i)
        if check.check_login==True:
            guest=i
            break
    myGuest = authenticate(request, username=guest.username, password='123456')
    auth.login(request, myGuest)
    check=GuestCheck.objects.get(user=guest)
    check.check_login=False
    check.save()
    return redirect('app:dashboard')
    