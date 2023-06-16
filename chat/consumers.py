import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message=='1234':
            async_to_sync(self.channel_layer.group_add)(
                "test1",
                self.channel_name
            )
            # self.accept()
            print('check111111')
        if message=='2345':
            async_to_sync(self.channel_layer.group_add)(
                "test2",
                self.channel_name
            )

        # async_to_sync(self.channel_layer.group_send)(
        #     'test1',
        #     {
        #         'type':'chat_message',
        #         'message':message
        #     }
        # )

        # async_to_sync(self.channel_layer.group_send)(
        #     'test',
        #     {
        #         'type':'chat_message',
        #         'message':'hello from server'
        #     }
        # )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))