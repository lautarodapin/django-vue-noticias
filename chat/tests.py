import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from api.routing import EntryDeMultiplexer
from chat.models import Room
from users.models import User
from rest_framework.authtoken.models import Token
from django.test import Client

class AuthWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, headers=None, subprotocols=None, user=None):
        super(AuthWebsocketCommunicator, self).__init__(application, path, headers, subprotocols)
        if user is not None:
            self.scope['user'] = user


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


    communicator = AuthWebsocketCommunicator(EntryDeMultiplexer.as_asgi(), f"/testws/", user=user)#?token={token.key}")
    # communicator.scope["user"] = user
    connected, subprotocol = await communicator.connect()
    assert connected

    
    await communicator.send_json_to(dict(
        stream="room",
        payload=dict(
            action="ping",
            request_id="test",
        )
    ))
    response = await communicator.receive_json_from()
    assert response == dict(payload="pong", stream="room")

    # 1. subscribe_instance
    await communicator.send_json_to(dict(
        stream="room",
        payload=dict(
            action="subscribe_instance",
            pk=room.pk,
            request_id="test",
        )
    ))
    response = await communicator.receive_json_from()
    assert response == dict(
        stream="room",
        payload=dict(
            action="subscribe_instance",
            data=None,
            errors=[],
            request_id="test",
            response_status=201
        )
    )

    # 2. subscribe_to_messages_in_room
    await communicator.send_json_to(dict(
        stream="room",
        payload=dict(
            action="subscribe_to_messages_in_room",
            pk=room.pk,
            request_id="test",
        )
    ))
    response = await communicator.receive_json_from()
    assert response == dict(payload="OK", stream="room")

    # 3. join_room
    await communicator.send_json_to(dict(
        stream="room",
        payload=dict(
            action="join_room",
            pk=room.pk,
            request_id="test",
        )
    ))
    response = await communicator.receive_json_from()
    assert response["stream"] == "room"
    assert response["payload"]["action"] == "update_users"    
    assert response["payload"]["data"][0]["email"] == user.email    
    assert response["payload"]["data"][0]["username"] == user.username   

    response = await communicator.receive_json_from()
    assert response["stream"] == "room"
    assert response["payload"]["action"] == "update_users"    
    assert response["payload"]["data"][0]["email"] == user.email    
    assert response["payload"]["data"][0]["username"] == user.username   

    # 4. Submit message test
    await communicator.send_json_to(dict(
        stream="room",
        payload=dict(
            action="create_message",
            message="test_message",
            request_id="test",
        )
    ))
    response = await communicator.receive_json_from()
    assert response.get("stream") == "room" 
    assert response.get("payload").get("action") == "create_message" 
    assert response.get("payload").get("request_id") == "test" 
    assert response.get("payload").get("response_status") == 200 

    # 5. Check if user is joined in the room.
    await database_sync_to_async(room.refresh_from_db)()
    current_user = await database_sync_to_async(room.current_users.first)()
    assert  current_user == user

    await communicator.disconnect()
