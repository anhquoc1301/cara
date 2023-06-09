from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your views here.

# def chat_message(self, event, type='chat_message'):
#     print("EVENT TRIGERED")

def lobby(request):
    channel_layer = get_channel_layer()
    # # data=test.objects.all().first()
    # a=str(data.value)
    # print(data)
    async_to_sync(channel_layer.group_send)(
        'test',
        {"type": "chat_message", "message": 'mama'},
    )
    return render(request, 'chat/lobby.html')

