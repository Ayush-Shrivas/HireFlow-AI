from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.accounts.models import User
from apps.notifications.services import create_notification
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


def user_conversations(user):
    return Conversation.objects.filter(participants=user).prefetch_related("participants", "messages__sender")


class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return user_conversations(self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participant_ids", [])
        if not isinstance(participant_ids, list) or request.user.id not in participant_ids or len(participant_ids) < 2:
            return Response({"detail": "A conversation needs at least two participants including you."}, status=status.HTTP_400_BAD_REQUEST)
        participants = list(User.objects.filter(id__in=participant_ids))
        if len(participants) != len(set(participant_ids)):
            return Response({"detail": "One or more participants do not exist."}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return Response(self.get_serializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_conversation(self):
        return get_object_or_404(Conversation, pk=self.kwargs["conversation_id"], participants=self.request.user)

    def get_queryset(self):
        return self.get_conversation().messages.select_related("sender")

    def perform_create(self, serializer):
        conversation = self.get_conversation()
        message = serializer.save(conversation=conversation, sender=self.request.user)
        conversation.save(update_fields=("updated_at",))
        for participant in conversation.participants.exclude(pk=self.request.user.pk):
            create_notification(participant, "MESSAGE_RECEIVED", "New message", f"{self.request.user.email} sent you a message.")


class MessageReadView(generics.UpdateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def patch(self, request, *args, **kwargs):
        message = self.get_object()
        message.read_at = timezone.now()
        message.save(update_fields=("read_at",))
        return Response(self.get_serializer(message).data)
