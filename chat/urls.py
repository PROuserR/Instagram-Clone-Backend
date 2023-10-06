from django.urls import path
from .views import *

app_name = 'chat'
urlpatterns = [
    path('list_chat/<int:my_id>/<int:peer_id>', list_chat, name='list_chat'),
    path('add_message/', add_message, name='add_message'),
]