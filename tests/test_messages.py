from typing import Tuple
import pytest
from rest_framework.test import APIClient

from chat.models import Message, Room
from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
import time

client = APIClient(enforce_csrf_checks=False)


def create_user() -> Tuple[User, Token]:
    user : User = User.objects.create_superuser(username="test", email="test@test.com", password="test")
    token : Token = Token.objects.create(user=user)
    return user, token

def create_room(host: User) -> Room:
    room : Room = Room.objects.create(nombre="test room", host=host)
    return room


@pytest.mark.django_db()
def test_create_message_in_room():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    room = create_room(user)
    
    response = client.get("/api/rooms/1/",)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("nombre") == room.nombre
    assert response.data.get("slug") == room.slug
    assert response.data.get("host").get("username") == user.username

    response = client.post("/api/messages/", data={
          "room":room.pk,
          "user":user.pk,
          "text":"test message",
    }, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get("text") == "test message"
    assert response.data.get("user") == user.pk
    assert response.data.get("room") == room.pk
    assert response.data.get("room_extra").get("nombre") == room.nombre
    assert response.data.get("user_extra").get("username") == user.username


@pytest.mark.django_db()
def test_get_messages_in_room():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    room = create_room(user)

    msg_1 : Message = Message.objects.create(user=user, room=room, text="test message 1")
    time.sleep(1)
    msg_2 : Message = Message.objects.create(user=user, room=room, text="test message 2")
    
    response = client.get("/api/rooms/1/",)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("nombre") == room.nombre
    assert response.data.get("slug") == room.slug
    assert response.data.get("host").get("username") == user.username
    assert response.data.get("last_message").get("id") == msg_2.pk
    assert response.data.get("messages")[0].get("id") == msg_1.pk
    assert response.data.get("messages")[1].get("id") == msg_2.pk