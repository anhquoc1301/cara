from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import test
import json
from django.http import HttpResponse
# Create your views here.

# def chat_message(self, event, type='chat_message'):
#     print("EVENT TRIGERED")

def lobby(request):
    channel_layer = get_channel_layer()
    data=test.objects.all().first()
    async_to_sync(channel_layer.group_send)(
        'test1',
        {"type": "chat_message", "message": "room test1"},
    )
    async_to_sync(channel_layer.group_send)(
        'test2',
        {"type": "chat_message", "message": "room test2"},
    )
    return render(request, 'chat/lobby.html')

def check(request, pk):
    channel_layer = get_channel_layer()
    print(pk)

    async_to_sync(channel_layer.group_add)(
        'test',
        'hjkfhekrjhgfk',
    )
    return HttpResponse('chiehfhj,sdfe')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def checkNickName(request):
    # request should be ajax and method should be GET.
    if is_ajax(request) and request.method == "GET":
        # get the nick name from the client side.
        nick_name = request.GET.get("nick_name", None)
        # check for the nick name in the database.
        print (nick_name)

    return render(request, 'chat/check.html')