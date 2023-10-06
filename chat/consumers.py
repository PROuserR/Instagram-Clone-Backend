import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.peer_id = self.scope['url_route']['kwargs']['peer_id']
        self.my_id = self.scope['url_route']['kwargs']['my_id']
        self.group_name = f'chat_{self.peer_id }_{self.my_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        image = text_data_json['image']
        peer_id = text_data_json['peer_id']
        my_id = text_data_json['my_id']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chatroom_message',
                'content': content,
                'image': image,
                'peer_id': peer_id,
                'my_id': my_id,
            }
        )

    async def chatroom_message(self, event):
        content = event['content']
        image = event['image']
        peer_id = event['peer_id']
        my_id = event['my_id']

        await self.send(text_data=json.dumps({
            'content': content,
            'image': image,
            'peer_id': peer_id,
            'my_id': my_id
        }))


users = []
class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'online_users'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        duplicates = False
        for u in users:
            if u['id'] == text_data_json['users']['id']:
                duplicates = True
                return
        if not duplicates and text_data_json['users']['id']:
            users.append(text_data_json['users'])
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'online_user_update',
                'users': users,
            }
        )

    async def online_user_update(self, event):
        user = event['users']
        
        await self.send(text_data=json.dumps({
            'users': user,
        }))