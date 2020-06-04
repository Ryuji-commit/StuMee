import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message, Channel
from stumee_study.models import Course
from stumee_auth.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.course_id = self.scope['url_route']['kwargs']['course_id']
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'chat_%s_%s' % (self.room_name, self.course_id)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        await self.create_message(event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def create_message(self, event):
        try:
            course = Course.objects.get(id=self.course_id)
            channel_user = CustomUser.objects.get(id=self.room_name)
            channel = Channel.objects.get(
                course__id=course.id,
                user__id=channel_user.id,
            )

            message = Message(
                channel=channel,
                user=self.user,
                content=event['message']
            )
            message.save()
        except Exception as e:
            raise




