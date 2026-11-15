from django.urls import path
from .views import ConversationListCreateView, MessageListCreateView, MessageReadView

urlpatterns = [
    path("", ConversationListCreateView.as_view(), name="conversation-list"),
    path("<int:conversation_id>/messages/", MessageListCreateView.as_view(), name="message-list"),
    path("messages/<int:pk>/read/", MessageReadView.as_view(), name="message-read"),
]
