# from os import path
from django.urls import re_path
from .consumers import AlertConsumer
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/alerts/', AlertConsumer.as_asgi()),
    re_path(r'ws/alerts/$', AlertConsumer.as_asgi()),
]
