from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
import json
from .models import User, ChatMessage
from .serializer import MessageSerializer
from .utils import LOGGER, get_user
from channels.db import database_sync_to_async


class PersonalChatConsimer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user: User = self.scope["user"]
        if self.user.is_authenticated:
            self.receiver_user = self.scope["url_route"]["kwargs"]["receiver_id"]
            user_ids = sorted([self.user.id, self.receiver_user])
            self.room_group_name = f'chat_{user_ids[0]}_{user_ids[1]}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        other_user = await get_user(self.scope["url_route"]["kwargs"]["receiver_id"])

        # Create a new message using async_to_sync for sync operations
        try:
            # Wrap ChatMessage.objects.create in async_to_sync
            chat_obj = await self.save_message_to_db(self.scope["user"], other_user, text_data)
        except Exception as e:
            LOGGER.warning(f"Error saving message {e}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": chat_obj
            }
        )
    
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        return await super().disconnect(code)
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def save_message_to_db(self, user, receiver, message):
        chat_obj = ChatMessage.objects.create(user=user, sender=user, receiver=receiver, message=message)
        chat_obj.save()
        return MessageSerializer(chat_obj).data
