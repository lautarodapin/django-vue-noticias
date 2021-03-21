from typing import Tuple
import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from api.routing import EntryDeMultiplexer
from users.models import User
from rest_framework.authtoken.models import Token
from django.test import Client
from todo.models import Todo
from rest_framework import status

class AuthWebsocketCommunicator(WebsocketCommunicator):
    def __init__(self, application, path, headers=None, subprotocols=None, user=None):
        super(AuthWebsocketCommunicator, self).__init__(application, path, headers, subprotocols)
        if user is not None:
            self.scope['user'] = user



@database_sync_to_async
def create_user(username: str="test", email: str="test@test.com", password:str = "test") -> Tuple[User, Token]:
    user : User = User.objects.create_superuser(username=username, email=email, password=password)
    token : Token = Token.objects.create(user=user)
    return user, token

@pytest.mark.django_db()
@pytest.mark.asyncio
async def test_todo_consumer():
    user, token = await create_user()
    user_2, token_2 = await create_user(username="test_2", email="test_2@test.com")
    todo_1 : Todo = await database_sync_to_async(Todo.objects.create)(user=user, title="todo")
    todo_2 : Todo = await database_sync_to_async(Todo.objects.create)(user=user_2, title="todo")
    communicator = AuthWebsocketCommunicator(EntryDeMultiplexer.as_asgi(), f"/testws/", user=user)
    connected, subprotocol = await communicator.connect()
    assert connected

    # Test LIST
    await communicator.send_json_to(dict(
        stream="todo",
        payload=dict(
            action="list",
            request_id=1,
        )
    ))
    response = await communicator.receive_json_from()
    assert response["stream"] == "todo"
    assert response["payload"]["action"] == "list"
    assert response["payload"]["response_status"] == status.HTTP_200_OK
    assert response["payload"]["errors"] == []
    assert response["payload"]["request_id"] == 1
    assert response["payload"]["data"].__len__() == 1
    assert response["payload"]["data"][0]["id"] == todo_1.pk
    assert response["payload"]["data"][0]["is_done"] == todo_1.is_done
    assert response["payload"]["data"][0]["title"]  == todo_1.title
    assert response["payload"]["data"][0]["user"]["id"] == user.pk 


    # Test RETRIEVE
    todo : Todo = await database_sync_to_async(Todo.objects.create)(user=user, title="todo")
    await communicator.send_json_to(dict(
        stream="todo",
        payload=dict(
            action="retrieve",
            request_id=1,
            pk=todo.pk
        )
    ))
    response = await communicator.receive_json_from()
    assert response["stream"] == "todo"
    assert response["payload"]["response_status"] == status.HTTP_200_OK
    assert response["payload"]["errors"] == []
    assert response["payload"]["request_id"] == 1
    assert response["payload"]["data"]["id"] == todo.pk
    assert response["payload"]["data"]["is_done"] == todo.is_done
    assert response["payload"]["data"]["title"]  == todo.title
    assert response["payload"]["data"]["user"]["id"] == user.pk 
    
    # Test CREATE
    await communicator.send_json_to(dict(
        stream="todo",
        payload=dict(
            action="create",
            data=dict(
                title="created_todo",
                user=user.pk,
            ),
            request_id=2,
        ),
    ))
    response = await communicator.receive_json_from()
    assert response["stream"] == "todo"
    assert response["payload"]["response_status"] == status.HTTP_201_CREATED
    assert response["payload"]["errors"] == []
    assert response["payload"]["request_id"] == 2
    assert response["payload"]["data"]["id"] == 4
    assert response["payload"]["data"]["is_done"] == False
    assert response["payload"]["data"]["title"] == "created_todo"
    assert response["payload"]["data"]["user"]["id"] == user.id

    # Test UPDATE
    await communicator.send_json_to(dict(
        stream="todo",
        payload=dict(
            action="update",
            request_id=3,
            pk=todo.pk,
            data=dict(
                user=user.pk,
                title="updated_todo",
                is_done=True,
            ),
        ),
    ))
    response = await communicator.receive_json_from()
    assert response["stream"] == "todo"
    assert response["payload"]["response_status"] == status.HTTP_200_OK
    assert response["payload"]["errors"] == []
    assert response["payload"]["request_id"] == 3
    assert response["payload"]["data"]["id"] == todo.pk
    assert response["payload"]["data"]["is_done"] == True
    assert response["payload"]["data"]["title"] == "updated_todo"
    assert response["payload"]["data"]["user"]["id"] == user.pk

    # Test DELETE
    await communicator.send_json_to(dict(
        stream="todo",
        payload=dict(
            action="delete",
            request_id=4,
            pk=todo.pk,
        ),
    ))
    response = await communicator.receive_json_from()
    assert response["payload"]["response_status"] == status.HTTP_204_NO_CONTENT

    await communicator.send_json_to(dict(
        stream="todo",
        payload=dict(
            action="subscribe_todos_in_user",
            request_id=5,
        ),
    ))
    response = await communicator.receive_json_from()
    
    assert response["payload"]["response_status"] == status.HTTP_200_OK
    assert response["payload"]["request_id"] == 5
    assert response["payload"]["errors"] == []
    assert response["payload"]["action"] == "subscribe_todos_in_user"


    await communicator.disconnect()
