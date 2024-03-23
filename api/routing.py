
from django.urls import re_path, path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security import AllowedHostsMiddleware

from .consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
    # re_path(r'^ws/chat/(?P<sender_id>\d+)/(?P<receiver_id>\d+)/$', ChatConsumer.as_asgi()),
]
