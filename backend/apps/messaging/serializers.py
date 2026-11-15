from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)

    class Meta:
        model = Message
        fields = ("id", "conversation", "sender", "sender_email", "body", "read_at", "created_at")
        read_only_fields = ("id", "conversation", "sender", "sender_email", "read_at", "created_at")


class ConversationSerializer(serializers.ModelSerializer):
    participant_ids = serializers.PrimaryKeyRelatedField(source="participants", many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "participant_ids", "last_message", "created_at", "updated_at")
        read_only_fields = fields

    def get_last_message(self, obj):
        message = obj.messages.select_related("sender").last()
        return MessageSerializer(message).data if message else None
