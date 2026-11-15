from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken

from .models import Conversation, Message


class ConversationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.user = await self.authenticate_query_token()
        if not self.user or not await self.is_participant():
            await self.close(code=4403)
            return
        self.group_name = f"conversation_{self.conversation_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        body = str(content.get("body", "")).strip()
        if not body:
            await self.send_json({"error": "Message body is required."})
            return
        message = await self.create_message(body)
        await self.channel_layer.group_send(self.group_name, {"type": "chat.message", "message": message})

    async def chat_message(self, event):
        await self.send_json(event["message"])

    async def authenticate_query_token(self):
        query = parse_qs(self.scope.get("query_string", b"").decode())
        raw_token = query.get("token", [""])[0]
        if not raw_token:
            return None
        try:
            validated = UntypedToken(raw_token)
            return await self.get_user(validated)
        except (AuthenticationFailed, InvalidToken, ValueError):
            return None

    @database_sync_to_async
    def get_user(self, validated):
        return JWTAuthentication().get_user(validated)

    @database_sync_to_async
    def is_participant(self):
        return Conversation.objects.filter(pk=self.conversation_id, participants=self.user).exists()

    @database_sync_to_async
    def create_message(self, body):
        message = Message.objects.create(conversation_id=self.conversation_id, sender=self.user, body=body)
        return {"id": message.id, "conversation": int(self.conversation_id), "sender": self.user.id, "sender_email": self.user.email, "body": message.body, "read_at": None, "created_at": message.created_at.isoformat()}
