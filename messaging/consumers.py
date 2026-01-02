import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message, GameInvite
from .serializers import MessageSerializer, GameInviteSerializer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"conversation_{self.conversation_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type=="message":
            message = await self.create_message(data["content"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message
                }
            )
        
        elif message_type=="invite":
            invite = await self.create_invite(data.get("content", ""))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "game_invite",
                    "invite": invite
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "data": event["message"]
        }))
    
    async def game_invite(self, event):
        await self.send(text_data=json.dumps({
            "type": "invite",
            "data": event["invite"]
        }))

    @database_sync_to_async
    def create_message(self, content):
        user = self.scope["user"]
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            content=content
        )

        return MessageSerializer(message).data

    @database_sync_to_async
    def create_invite(self, content):
        user = self.scope["user"]
        conversation = Conversation.objects.get(id=self.conversation_id)
        invite = GameInvite.objects.create(
            conversation=conversation,
            sender=user,
            content=content
        )

        return GameInviteSerializer(invite).data