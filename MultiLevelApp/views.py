from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .models import Deal, User, InputCoin, OutputCoin, BetDeal
import random
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
import time
from .decorators import admin_only
# from .check import checkSum
# Create your views here.


class register(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'dangky/dangky.html')
        else:
            return redirect('app1:home')
    def post(self, request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            password2=request.POST.get('password2')
            email=request.POST.get('email')
            referrer=None
            if request.POST.get('referrer'):
                referrer=int(request.POST.get('referrer'))
            code=random.randint(100000000, 999999999)
            while User.objects.filter(code=code).exists():
                code = random.randint(100000000, 999999999)
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Tên đăng nhập trùng!')
                return redirect('app1:register')
            if password==password2:
                ur=User.objects.create_user(username=username, password=password, email=email)
                if referrer is not None:
                    ur.referrer=referrer
                    ur.referrer_temporary=referrer
                ur.code=code
                ur.coin=10000000
                ur.total_deal=0
                ur.bonuscoin=0
                ur.save()
                messages.success(request, 'Đăng ký thành công!')
                return redirect('app1:login')
            else:
                messages.warning(request, 'Mật khẩu không khớp!')
                return redirect('app1:register')





class login(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'dangnhap/dangnhap.html')
        else:
            return redirect('app1:home')
    def post(self,request):
        username = request.POST.get('username')
        password= request.POST.get('password')
        my_user = authenticate(request, username=username,password=password)
        if my_user is None:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu!')
            return redirect('app1:login')
        else:
            auth.login(request, my_user)
            return redirect('app1:home')



@login_required
def logout(request):
    auth.logout(request)
    return redirect('app1:login')





@login_required
def inputcoin(request):
    if request.method=="POST":
        prime=int(request.POST.get('prime'))
        print(prime)
        print(type(prime))
        ip=InputCoin.objects.create(coin_deal=prime, user=request.user.code)
        ur=User.objects.get(id=request.user.id)
        ur.coin=ur.coin+prime
        ur.save()
        ip.save()
        messages.success(request, 'Nạp tiền thành công!')
    return render(request, 'inputcoin.html')



@login_required
def outputcoin(request):
    if request.method=="POST":
        prime=int(request.POST.get('prime'))
        ur=User.objects.get(id=request.user.id)
        if ur.coin>=prime:
            ur.coin-=prime
            ur.save()
            ip=OutputCoin.objects.create(coin_deal=prime, user=request.user.code)
            ip.save()
            messages.success(request, 'Rút tiền thành công!')
            return redirect('app1:outputcoin')
        else:
            messages.warning(request, 'Rút tiền thất bại!')
            return redirect('app1:outputcoin')
    return render(request, 'outputcoin.html')



@login_required
def deal(request):
    if request.method=="POST":
        prime=int(request.POST.get('prime'))
        unto=int(request.POST.get('unto'))
        ur=User.objects.get(id=request.user.id)
        to=User.objects.get(code=unto)
        if ur.coin>=prime:
            ur.coin-=prime
            to.coin+=prime
            to.save()
            ur.save()
            ip=Deal.objects.create(coin_deal=prime,unto=unto, user=request.user.code)
            ip.save()
            messages.success(request, 'Chuyển khoản thành công!')
            return redirect('app1:deal')
        else:
            messages.warning(request, 'Chuyển khoản thất bại!')
            return redirect('app1:deal')
    return render(request, 'deal.html')



@login_required
def editpassword(request):
    ur=User.objects.get(id=request.user.id)
    if request.method=="POST":
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
                ur.set_password(password2)
                ur.save()
                messages.success(request, 'Đổi mật khẩu thành công!')
                ur2=authenticate(username=ur.username, password=password2)
                auth.login(request, ur2)
                return redirect('app1:home')
        else:
            messages.warning('Mật khẩu không khớp!')
            return redirect('app1:editpassword')
    return render(request, 'editpassword.html')



@login_required
def viewcoin(request):
    ur=User.objects.get(id=request.user.id)
    return render(request, 'viewcoin.html', {'form':ur})



def checkSum(code):
    sum = 0
    a = []
    ur = User.objects.all()
    for i in ur:
        if i.referrer_temporary == code:
            a.append(i.code)
    for i in a:
        for j in ur:
            if i == j.code:
                sum+=j.total_deal+checkSum(i)
    return sum



def autocheck():
    ur=User.objects.all()
    for i in ur:
        k = 0
        total=checkSum(i.code)
        for j in ur:
            if j.referrer_temporary == i.code and j.total_deal >= 500:
                k += 1
        if i.level<1:
            if k>=3 and i.total_deal>=500 and total>=20000:
                i.level=1
                i.bonus=0.7/100
                i.save()
                for j in ur:
                    if j.referrer==i.code and i.level>=j.level:
                        j.referrer_temporary=i.code
                        j.save()
        if i.level<2:
            if k >=5  and i.total_deal >= 1000 and total >= 100000:
                i.level = 2
                i.bonus = 0.8 / 100
                i.save()
                for j in ur:
                    if j.referrer==i.code and i.level>=j.level:
                        j.referrer_temporary=i.code
                        j.save()
        if i.level<3:
            if k >= 10 and i.total_deal >= 5000 and total >= 500000:
                i.level = 3
                i.bonus = 0.9 / 100
                i.save()
                for j in ur:
                    if j.referrer==i.code and i.level>=j.level:
                        j.referrer_temporary=i.code
                        j.save()
        if i.level<4:
            if k >= 15 and i.total_deal >= 10000 and total >= 3500000:
                i.level = 4
                i.bonus = 1 / 100
                i.save()
                for j in ur:
                    if j.referrer==i.code and i.level>=j.level:
                        j.referrer_temporary=i.code
                        j.save()
        if i.level<5:
            h = 0
            for j in ur:
                if j.referrer_temporary == i.code and j.total_deal >= 1000:
                    h += 1
            if h >= 20 and i.total_deal >= 20000 and total >= 10000000:
                i.level = 5
                i.bonus = 1.2 / 100
                i.save()
                for j in ur:
                    if j.referrer==i.code and i.level>=j.level:
                        j.referrer_temporary=i.code
                        j.save()
#     set_dad
    for i in ur:
        if i.referrer_temporary is not None:
            a=i.referrer_temporary
            dad=User.objects.get(code=a)
            if i.level <= dad.level:
                i.referrer_temporary=dad.code
            if i.level>dad.level:
                if dad.referrer_temporary is not None:
                    b = dad.referrer_temporary
                    k = 1
                    while k == 1:
                        dadn=User.objects.get(code=b)
                        if i.level>dadn.level:
                            if dadn.referrer_temporary is not None:
                                b=dadn.referrer_temporary
                            else:
                                i.referrer_temporary=None
                                k=2
                        else:
                            i.referrer_temporary=dadn.code
                            k=2

                else:
                    i.referrer_temporary=None

    for h in ur:
            h.bonuscoin=0
            h.save()

  
def check():
    a=[]
    ur=User.objects.all()
    for i in ur:
        a.append(i)
    a.reverse()
    for i in a:
        print(i.create_at)
autocheck()


@login_required
def historyoutput(request):
    ur=OutputCoin.objects.filter(user=request.user.code)
    context={'form': ur}
    return render(request, 'history/historyoutput.html', context)
@login_required
def historyinput(request):
    ur=InputCoin.objects.filter(user=request.user.code)
    context={'form': ur}
    return render(request, 'history/historyinput.html', context)
@login_required
def historydeal(request):
    ur=Deal.objects.filter(user=request.user.code)
    context={'form': ur}
    return render(request, 'history/historydeal.html', context)
@login_required
def historybet(request):
    ur=BetDeal.objects.filter(user=request.user.code)
    context={'form': ur}
    return render(request, 'history/historybet.html', context)

@login_required
def historyreceive(request):
    ur=Deal.objects.filter(unto=request.user.code)
    context={'form': ur}
    return render(request, 'history/historyreceive.html', context)



@login_required
def listchild(request):
    if request.user.username=='admin':
        return redirect('app1:onlyadmin')
    us=User.objects.get(code=request.user.code)
    b=float(int(us.bonuscoin*10)/10)
    ur=User.objects.all()
    total = checkSum(request.user.code)
    a=[]
    for i in ur:
        if i.referrer_temporary==request.user.code:
            a.append(i)
    context={'form':a, 'total':total, 'bonus':b, 'us':us }
    return render(request,'home/home.html', context)



@login_required
def listf(request, pk):
    us=User.objects.get(code=request.user.code)
    b=float(int(us.bonuscoin*10)/10)
    ur=User.objects.all()
    total=checkSum(request.user.code)
    us=User.objects.get(code=pk)
    a=[]
    for i in ur:
        if i.referrer_temporary==us.code:
            a.append(i)
    context={'form':a, 'total':total,'bonus':b }
    return render(request,'viewf.html', context)


@login_required
def bet_view(request):
        if request.method=='POST':
            prime=int(request.POST.get('prime'))
            ur=User.objects.get(id=request.user.id)
            if ur.coin>=prime:
                betdeal=BetDeal.objects.create(coin_deal=prime, user=ur.code)
                betdeal.save()
                ur.total_deal+=int(prime)
                ur.coin=ur.coin-int(prime)
                ur.save()
                messages.success(request, 'Cược thành công!')
                return redirect('app1:bet_view')
            else:
                messages.warning(request, 'Cược thất bại!')
                return redirect('app1:bet_view')
        return render(request, 'bet/bet.html')


@login_required
@admin_only
def onlyadmin(request):
    ur=User.objects.all()
    total=0
    bonus=0
    lv0=lv1=lv2=lv3=lv4=lv5=0
    for i in ur:
        total+=i.total_deal
        bonus+=i.bonuscoin
    bonus=float(int(bonus * 10) / 10)
    for i in ur:
        if i.level==0:
            lv0+=1
        if i.level==1:
            lv1+=1
        if i.level==2:
            lv2+=1
        if i.level==3:
            lv3+=1
        if i.level==4:
            lv4+=1
        if i.level==5:
            lv5+=1
    context={'total': total, 'bonus':bonus, 'lv0': lv0, 'lv1': lv1, 'lv2': lv2, 'lv3': lv3, 'lv4': lv4, 'lv5': lv5}
    return render(request, 'onlyadmin.html', context)


@login_required
def resetweek(request):
    ur = User.objects.all()
    if request.method=="POST":
        for i in ur:
            i.coin+=i.bonuscoin
            i.total_deal = 0
            i.bonus=0
            i.level = 0
            i.bonuscoin = 0
            i.referrer_temporary = i.referrer
            i.save()
        messages.success(request,'Reset lại thành công')
        return redirect('app1:onlyadmin')
    return render(request, 'resetweek.html')
