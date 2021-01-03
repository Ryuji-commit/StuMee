import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from django.core.mail import send_mail

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
        user_id = text_data_json['user_id']
        user_img = text_data_json['user_img']
        user_name = text_data_json['user_name']
        message_type = text_data_json['message_type']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'user_img': user_img,
                'user_name': user_name,
                'message_type': message_type,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_img = event['user_img']
        user_name = event['user_name']
        message_type = event['message_type']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'user_img': user_img,
            'user_name': user_name,
            'message_type': message_type,
        }))
        if self.user.id == user_id and message_type != "ENTERING":
            await self.create_message(message)

    @database_sync_to_async
    def create_message(self, message):
        try:
            course = Course.objects.get(id=self.course_id)
            channel_user = CustomUser.objects.get(id=self.room_name)
            channel = Channel.objects.get(
                course__id=course.id,
                user__id=channel_user.id,
                is_discussion=False,
            )

            if self.user == channel_user:
                channel.is_active = True
                if len(message) >= 30 and 'class="posted-' not in message:
                    email_subject = "{}さんから質問がありました".format(channel_user.username)
                    email_message = "コース名[{}]にて、{}さんから新規の質問がありました。\n\n質問内容: {}"\
                        .format(course.title, channel_user.username, message)
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = list(course.staffs.values_list('email', flat=True))
                    if course.create_user.email:
                        recipient_list.append(course.create_user.email)
                    send_mail(email_subject, email_message, from_email, recipient_list)
            else:
                channel.is_active = False
            channel.save()

            message = Message(
                channel=channel,
                user=self.user,
                content=message
            )
            message.save()
        except Exception as e:
            raise


class DiscussionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'discussion_%s' % self.room_name

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
        user_id = text_data_json['user_id']
        user_img = text_data_json['user_img']
        user_name = text_data_json['user_name']
        message_type = text_data_json['message_type']
        if message_type != "ENTERING":
            await self.create_message(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'user_img': user_img,
                'user_name': user_name,
                'message_type': message_type,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_img = event['user_img']
        user_name = event['user_name']
        message_type = event['message_type']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'user_img': user_img,
            'user_name': user_name,
            'message_type': message_type,
        }))

    @database_sync_to_async
    def create_message(self, message):
        try:
            course = Course.objects.get(id=self.room_name)
            channel_user = course.create_user
            channel = Channel.objects.get(
                course__id=course.id,
                user__id=channel_user.id,
                is_discussion=True,
            )

            message = Message(
                channel=channel,
                user=self.user,
                content=message
            )
            message.save()
        except Exception as e:
            raise




