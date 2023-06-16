from django.urls import path 
from . import views 
from .views import check, checkNickName

urlpatterns = [
    path('', views.lobby),
    path(r'^check/(?P<pk>\w+)$', check, name='check'),
    path('nickname/', checkNickName, name = "validate_nickname")


]