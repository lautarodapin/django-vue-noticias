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



@database_sync_to_async
def create_user() -> Tuple[User, Token]:
    user : User = User.objects.create_superuser(username="test", email="test@test.com", password="test")
    room : Room = Room.objects.create(nombre="test room", host=user)
    return user, room



@pytest.mark.django_db()
@pytest.mark.asyncio
def test_register_user():
    response: WSGIRequest = client.post("/api/users/", data={
        "username":"test_user",
        "password":"test_password"
    }, format="json",)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get("username") == "test_user"

    
@pytest.mark.django_db()
@pytest.mark.asyncio
def test_get_users():
    client.post("/api/users/", data={
        "username":"test_user",
        "password":"test_password"
    }, format="json",)
    response = client.get(f"/api/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["id"] == 1
    assert response.data[0]["username"] == "test_user"
    

@pytest.mark.django_db()
@pytest.mark.asyncio
def test_get_user():
    client.post("/api/users/", data={
        "username":"test_user",
        "password":"test_password"
    }, format="json",)
    response = client.get(f"/api/users/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == 1
    assert response.data["username"] == "test_user"

@pytest.mark.django_db()
@pytest.mark.asyncio
def test_put_user():
    client.post("/api/users/", data={
        "username":"test_user",
        "password":"test_password"
    }, format="json",)
    response = client.put(f"/api/users/1/", data={
        "username":"edited_test_username"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == 1
    assert response.data["username"] == "edited_test_username"


@pytest.mark.django_db()
@pytest.mark.asyncio
def test_delete_user():
    client.post("/api/users/", data={
        "username":"test_user",
        "password":"test_password"
    }, format="json",)
    response = client.delete(f"/api/users/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/api/users/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND