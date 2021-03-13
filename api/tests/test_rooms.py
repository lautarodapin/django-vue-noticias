from typing import Tuple
from django.core.handlers.wsgi import WSGIRequest
import pytest
from rest_framework.test import APIClient


from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from api.routing import EntryDeMultiplexer
from chat.models import Room
from users.models import User
from rest_framework.authtoken.models import Token
from django.test import Client
from rest_framework import status

client = APIClient()


"""
TODO     El usuario tiene q ser scopeado a este archivo
"""

# @pytest.mark.django_db(transaction=True)
# @pytest.mark.asyncio
# def test_create_room():
#     response = client.post("/api/users/", data={
#         "username":"test_user",
#         "password":"test_password"
#     })
#     assert response.status_code == status.HTTP_201_CREATED

#     client.login(username="test_user", password="test_password")
#     response: WSGIRequest = client.post("/api/rooms/", data={
#         "nombre":"test_room",
#     }, format="json",)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data.get("username") == "test_user"
