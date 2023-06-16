# from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
# import json
# from channels.db import database_sync_to_async
# from .models import Statistic, DataItem

# class DashboardConsumer(WebsocketConsumer):
#     async def connect(self):
#         print(dashboard_slug)
#         # dashboard_slug = self.scope['url_route']['kwargs']['dashboard_slug']
#         dashboard_slug='main'
#         self.dashboard_slug = dashboard_slug
#         self.room_group_name = f'ModuleApp-{dashboard_slug}'
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     # async def disconnect(self, close_code):
#     #     print(f'connection closed with code: {close_code}')
#     #     await self.channel_layer.group_discard(
#     #         self.room_group_name,
#     #         self.channel_layer,
#     #     )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = text_data_json['sender']

#         print(message)
#         print(sender)

#         dashboard_slug= self.dashboard_slug

#         await self.save_data_item(sender, message, dashboard_slug)

#         await self.channel_layer.group_send(self.room_group_name, {
#             'type': 'statistics_message',
#             'message': message,
#             'sender': sender,
#         })


#     async def statistics_message(self, event):
#         message = event['message']
#         sender = event['sender']

#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender,
#         }))
#     @database_sync_to_async
#     def create_data_item(self, sender, message, slug):
#         obj = Statistic.objects.get(slug=slug)
#         return DataItem.objects.create(statistic=obj, value = message, owner=sender)
    
#     async def save_data_item(self, sender, message, slug):
#         await self.create_data_item(sender, message, slug)             

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            str(self.room_group_name),
            self.channel_name
        )
        self.accept()
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message=='normal':
            async_to_sync(self.channel_layer.group_add)(
                "normal",
                self.channel_name
            )
        if message=='vip':
            async_to_sync(self.channel_layer.group_add)(
                "vip",
                self.channel_name
            )
        if message=='superior':
            async_to_sync(self.channel_layer.group_add)(
                "superior",
                self.channel_name
            )
        if message=='super_vip':
            async_to_sync(self.channel_layer.group_add)(
                "super_vip",
                self.channel_name
            )

        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type':'chat_message',
        #         'message':message
        #     }
        # )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))