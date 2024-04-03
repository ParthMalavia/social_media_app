from django.urls import path
from .consumer import PersonalChatConsimer


websocket_urlpatterns = [
    path("ws/chat/<int:receiver_id>/", PersonalChatConsimer.as_asgi())
]