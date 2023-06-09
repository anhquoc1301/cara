from django.urls import path
from .views import register, login, bet_view, logout
from .views import deal, inputcoin, outputcoin, editpassword, viewcoin
from .views import historybet, historydeal, historyinput, historyoutput, historyreceive
from .views import listchild, listf, onlyadmin, resetweek
app_name='app1'
urlpatterns = [
    path('register/', register.as_view(), name='register'),
    path('', login.as_view(), name='login'),
    path('bet_view/', bet_view, name='bet_view'),
    path('logout/', logout, name='logout'),
    path('deal/', deal, name='deal'),
    path('inputcoin/', inputcoin, name='inputcoin'),
    path('outputcoin/', outputcoin, name='outputcoin'),
    path('editpassword/', editpassword, name='editpassword'),
    path('viewcoin/', viewcoin, name='viewcoin'),
    path('historybet/', historybet, name='historybet'),
    path('historydeal/', historydeal, name='historydeal'),
    path('historyinput/', historyinput, name='historyinput'),
    path('historyoutput/', historyoutput, name='historyoutput'),
    path('historyreceive/', historyreceive, name='historyreceive'),
    path('home/', listchild, name='home'),
    path('listf/<str:pk>/', listf, name='listf'),
    path('onlyadmin/', onlyadmin, name='onlyadmin'),
    path('resetweek/', resetweek, name='resetweek'),

]