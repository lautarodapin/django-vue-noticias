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
def test_create_room():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    response = client.post("/api/rooms/", data={
        "nombre":"test room",
    }, format="json",)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get("nombre") == "test room"
    assert response.data.get("slug") == f"test-room-{user.username}"
    assert response.data.get("host").get("username") == user.username


@pytest.mark.django_db()
@pytest.mark.asyncio
def test_get_rooms():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    room : Room = Room.objects.create(nombre="test room", host=user)

    response = client.get("/api/rooms/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0].get("nombre") == room.nombre
    assert response.data[0].get("slug") == room.slug
    assert response.data[0].get("host").get("username") == user.username


@pytest.mark.django_db()
@pytest.mark.asyncio
def test_get_room():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    room : Room = Room.objects.create(nombre="test room", host=user)

    response = client.get("/api/rooms/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("nombre") == room.nombre
    assert response.data.get("slug") == room.slug
    assert response.data.get("host").get("username") == user.username


@pytest.mark.django_db()
@pytest.mark.asyncio
def test_put_room():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    room : Room = Room.objects.create(nombre="test room", host=user)

    response = client.put("/api/rooms/1/", data={
        "nombre":"test room edited"
    }, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("nombre") == "test room edited"
    assert response.data.get("slug") == f"test-room-edited-{user.username}"
    assert response.data.get("host").get("username") == user.username



@pytest.mark.django_db()
@pytest.mark.asyncio
def test_delete_room():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    room : Room = Room.objects.create(nombre="test room", host=user)

    response = client.delete("/api/rooms/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/api/rooms/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
