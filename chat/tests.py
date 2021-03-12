import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from api.routing import EntryDeMultiplexer
from chat.models import Room
from users.models import User
from rest_framework.authtoken.models import Token
from django.test import Client



@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_my_consumer():

    communicator = WebsocketCommunicator(EntryDeMultiplexer.as_asgi(), "/testws/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_database():
    user : User = await database_sync_to_async(User.objects.create_superuser)(username="test", email="test@test.com", password="test")
    _user = await database_sync_to_async(User.objects.get)(username="test")
    assert user == _user

def headers_from_client(client):
    """Builds headers to send with WebSocket requests from a HTTP client."""
    return [
        (b"origin", b"..."),
        (b"cookie", client.cookies.output(header="", sep="; ").encode()),
    ]
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_room_consumer():
    user : User = await database_sync_to_async(User.objects.create_superuser)(username="test", email="test@test.com", password="test")
    room : Room = await database_sync_to_async(Room.objects.create)(nombre="test room", host=user)
    token : Token = await database_sync_to_async(Token.objects.create)(user=user)

    client = Client()
    await database_sync_to_async(client.force_login)(user)

    communicator = WebsocketCommunicator(EntryDeMultiplexer.as_asgi(), f"/testws/", headers_from_client(client))#?token={token.key}")
    # communicator.scope["user"] = user
    connected, subprotocol = await communicator.connect()
    assert connected

    
    await communicator.send_json_to(dict(
        stream="room",
        payload=dict(
            action="join_room",
            pk=room.pk,
            request_id="test",
        )
    ))

    response = await communicator.receive_json_from(timeout=10)
    assert response == {
                        "stream":"user",
                        "payload":{
                            "pk":user.pk
                        }
                    }
    
    await database_sync_to_async(room.refresh_from_db)()
    current_user = await database_sync_to_async(room.current_users.first)()
    assert  current_user == user

    await communicator.disconnect()
