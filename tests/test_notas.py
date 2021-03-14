from typing import Tuple
from django.core.handlers.wsgi import WSGIRequest
import pytest
from rest_framework.test import APIClient


from users.models import User
from rest_framework.authtoken.models import Token
from news.models import Nota, Comentario
from rest_framework import status
from dataclasses import dataclass
from django.utils.timezone import now



client = APIClient(enforce_csrf_checks=False)



def create_user() -> Tuple[User, Token]:
    user : User = User.objects.create_superuser(username="test", email="test@test.com", password="test")
    token : Token = Token.objects.create(user=user)
    return user, token


@pytest.mark.django_db()
def test_create_nota():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    response = client.post("/api/nota/", data=dict(
        titulo="titulo test",
        subtitulo="subtitulo test",
        cuerpo="cuerpo test",
        autor=user.pk
    ))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["titulo"] == "titulo test"
    assert response.data["subtitulo"] == "subtitulo test"
    assert response.data["cuerpo"] == "cuerpo test"
    assert response.data["autor"] == user.pk
    assert response.data["slug"] == f"{now().strftime('%Y-%m-%d')}-titulo-test-{user.username}"