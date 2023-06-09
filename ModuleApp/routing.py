from django.urls import re_path
from .consumers import DashboardConsumer

websocket_urlpatterns = [
    re_path(r'ws/invest', DashboardConsumer.as_asgi()),
]