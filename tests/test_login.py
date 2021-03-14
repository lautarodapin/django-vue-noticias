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

client = APIClient(enforce_csrf_checks=False)



def create_user() -> Tuple[User, Token]:
    user : User = User.objects.create_superuser(username="test", email="test@test.com", password="test")
    token : Token = Token.objects.create(user=user)
    return user, token


@pytest.mark.django_db()
@pytest.mark.asyncio
def test_login():
    user, token = create_user()
    
    response = client.post("/api/auth/", data={
        "username":"test",
        "password":"test",
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["username"] == user.username
    assert response.data["token"] == token.key


@pytest.mark.django_db()
def test_register():
    response = client.post("/api/users/", data={
        "username":"test",
        "password":"test",
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "test"

@pytest.mark.django_db()
def test_get_csrf_token():
    response : WSGIRequest= client.get("/api/get-csrf-token/")
    assert response.status_code == status.HTTP_200_OK
    assert "csrftoken" in response.cookies