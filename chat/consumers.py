import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, User, Room, Group


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = "chat_%s" % self.chat_box_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room = text_data_json["room"]
        category = text_data_json["category"]

        await self.save_message(username, room, message, category)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message", 
                "message": message,
                "username": username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )
    
    @sync_to_async
    def save_message(self, username, room, message, category):
        if category == "room":
            user = User.objects.get(username=username)
            room = Room.objects.get(slug=room)

            Message.objects.create(user=user, room=room, content=message)
        if category == "group":
            user = User.objects.get(username=username)
            group = Group.objects.get(slug=room)

            Message.objects.create(user=user, group=group, content=message)