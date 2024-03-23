import json

from json import JSONDecodeError
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("connect >>> ", self.scope, "<<<<<")
        # Authenticate and get user
        try:
            token = self.scope["headers"]["authorization"].decode("utf-8").split()[1]
            user = await database_sync_to_async(User.objects.get_by_natural_key)(token)
        except (KeyError, User.DoesNotExist, JSONDecodeError):
            await self.close(code=403)  # Unauthorized access
            return

        # Get chat participants from URL path
        sender_id = self.scope["url_route"]["kwargs"]["sender_id"]
        receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]

        # Validate participants
        if user.id not in [int(sender_id), int(receiver_id)]:
            await self.close(code=403)  # Unauthorized access
            return

        # Check if chat group exists, create if needed
        group_name = f"chat_{sender_id}_{receiver_id}"
        await self.channel_layer.group_add(group_name, self.channel_name)

        # Set initial page number for pagination
        self.page_number = 1

        # Accept the connection
        await self.accept()

        # Send initial messages (latest 20)
        await self.send_initial_messages(group_name)

    async def send_initial_messages(self, group_name):
        print("send_initial_messages >>> ")
        messages = await database_sync_to_async(ChatMessage.objects.filter(
            sender__id__in=[self.scope["url_route"]["kwargs"]["sender_id"], self.scope["url_route"]["kwargs"]["receiver_id"]],
            receiver__id__in=[self.scope["url_route"]["kwargs"]["sender_id"], self.scope["url_route"]["kwargs"]["receiver_id"]],
        ).order_by('-date')[:20])  # Latest 20 messages
        for message in messages:
            await self.channel_layer.group_send(
                group_name,
                {
                    "type": "chat_message",
                    "content": message.serialize(),
                }
            )

    async def receive(self, text_data):
        print("receive >>> ", text_data)
        try:
            data = json.loads(text_data)
            message = data.get("message")
            action = data.get("action")
        except JSONDecodeError:
            return

        if message:
            await self.create_message(message)
        elif action == "load_more":
            await self.send_older_messages()

    async def create_message(self, message):
        print("create_message >>> ", message)
        sender_id = int(self.scope["url_route"]["kwargs"]["sender_id"])
        receiver_id = int(self.scope["url_route"]["kwargs"]["receiver_id"])

        message_obj = await database_sync_to_async(ChatMessage.objects.create)(
            user=self.scope["user"],
            sender=User.objects.get(id=sender_id),
            receiver=User.objects.get(id=receiver_id),
            message=message,
        )

        await self.channel_layer.group_send(
            f"chat_{sender_id}_{receiver_id}",
            {
                "type": "chat_message",
                "content": message_obj.serialize(),
            }
        )

    async def send_older_messages(self):
        print("send_older_messages >>> ")
        sender_id = int(self.scope["url_route"]["kwargs"]["sender_id"])
        receiver_id = int(self.scope["url_route"]["kwargs"]["receiver_id"])

        messages = await database_sync_to_async(ChatMessage.objects.filter(
            sender__id__in=[sender_id, receiver_id],
            receiver__id__in=[sender_id, receiver_id],
        ).order_by('-date')[self.page_number * 20: (self.page_number + 1) * 20])  # Fetch next 20 messages

        if messages:
            self.page_number += 1
            for message in messages:
                await self.channel_layer.group_send(
                    f"chat_{sender_id}_{receiver_id}",
                    {
                        "type": "chat_message",
                        "content": message.serialize(),
                    }
                )

    async def disconnect(self, code):
        print("disconnect >>> ")
        # Remove channel from the group on disconnect
        sender_id = int(self.scope["url_route"]["kwargs"]["sender_id"])
        receiver_id = int(self.scope["url_route"]["kwargs"]["receiver_id"])
        await self.channel_layer.group_discard(f"chat_{sender_id}_{receiver_id}", self.channel_name)
