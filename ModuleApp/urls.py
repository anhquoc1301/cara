from django.urls import path
from .views import main, chart_data, home, login, logout, register, change_password, edit_password_wallet
from .views import dashboard, wallet, add_method, input_money, output_money, history_input, history_output
from .views import list_accept_input_money, accept_input_money, cancel_status_input_money, list_accept_output_money
from .views import cancel_status_output_money, accept_status_output_money, list_staff, list_user
from .views import list_user_not_referrer, set_user_referrer, add_staff, service, invest, cron, guest_login
app_name='app'
urlpatterns = [
    path('main/', main, name='main'),
    path('home/', home, name='home'),
    path('service/', service, name='service'),
    path('', login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register.as_view(), name='register'),
    path('change_password/', change_password, name='change_password'),
    path('edit_password_wallet/', edit_password_wallet, name='edit_password_wallet'),
    path('dashboard/', dashboard, name='dashboard'),
    path('wallet/', wallet, name='wallet'),
    path('add_method/', add_method, name='add_method'),
    path('input_money/', input_money, name='input_money'),
    path('output_money/', output_money, name='output_money'),
    path('history_input/', history_input, name='history_input'),
    path('history_output/', history_output, name='history_output'),
    path('list_accept_input_money/', list_accept_input_money, name='list_accept_input_money'),
    path('accept_input_money/<str:pk>/', accept_input_money, name='accept_input_money'),
    path('cancel_status_input_money/<str:pk>/', cancel_status_input_money, name='cancel_status_input_money'),
    path('list_accept_output_money/', list_accept_output_money, name='list_accept_output_money'),
    path('cancel_status_output_money/<str:pk>/', cancel_status_output_money, name='cancel_status_output_money'),
    path('accept_status_output_money/<str:pk>/', accept_status_output_money, name='accept_status_output_money'),
    path('list_staff/', list_staff, name='list_staff'),
    path('list_user/', list_user, name='list_user'),
    path('list_user_not_referrer/', list_user_not_referrer, name='list_user_not_referrer'),
    path('set_user_referrer/<str:pk>/', set_user_referrer, name='set_user_referrer'),
    path('add_staff/', add_staff, name='add_staff'),
    path('invest/', invest, name='invest'),
    path('cron/', cron, name='cron'),
    path('guest_login/', guest_login, name='guest_login'),
]