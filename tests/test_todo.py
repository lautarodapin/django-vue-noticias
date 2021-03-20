from typing import Tuple
import pytest
from rest_framework.test import APIClient


from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from todo.models import Todo

client = APIClient(enforce_csrf_checks=False)



def create_user() -> Tuple[User, Token]:
    user : User = User.objects.create_superuser(username="test", email="test@test.com", password="test")
    token : Token = Token.objects.create(user=user)
    return user, token


@pytest.mark.django_db()
@pytest.mark.asyncio
def test_create_todo():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    response = client.post("/api/todos/", data={
        "user":user.pk,
        "title":"todo test",
    }, format="json",)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get("title") == "todo test"
    assert response.data.get("user").get("id") == user.pk

@pytest.mark.django_db()
@pytest.mark.asyncio
def test_get_todos():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    todo : Todo = Todo.objects.create(title="test todo", user=user)

    response = client.get("/api/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0].get("title") == todo.title
    assert response.data[0].get("user").get("id") == todo.user.pk


@pytest.mark.django_db()
@pytest.mark.asyncio
def test_get_todo():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    todo : Todo = Todo.objects.create(title="test todo", user=user)

    response = client.get("/api/todos/1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("title") == todo.title
    assert response.data.get("user").get("id") == todo.user.pk


@pytest.mark.django_db()
def test_put_todo():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    todo : Todo = Todo.objects.create(title="test todo", user=user)
    response = client.put("/api/todos/1/", data={
        "title":"test todo edited",
        "is_done":True,
        "user":user.id
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("title") == "test todo edited"
    assert response.data.get("is_done") == True
    assert response.data.get("user").get("id") == user.pk


@pytest.mark.django_db()
def test_delete_todo():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    todo : Todo = Todo.objects.create(title="test todo", user=user)

    response = client.delete("/api/todos/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/api/todos/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
