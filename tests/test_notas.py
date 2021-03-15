from typing import List, Tuple
from django.core.handlers.wsgi import WSGIRequest
import pytest
from rest_framework.test import APIClient
import time

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


@pytest.mark.django_db()
def test_get_notas():
    user, token = create_user()
    nota_1 : Nota = Nota.objects.create(titulo="titulo 1", subtitulo="subtitulo 1", cuerpo="cuerpo 1", autor=user)
    nota_2 : Nota = Nota.objects.create(titulo="titulo 2", subtitulo="subtitulo 2", cuerpo="cuerpo 2", autor=user)
    client.credentials(HTTP_AUTHORIZATION="")
    response = client.get("/api/nota/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data.__len__() == 2
    assert response.data[0]["titulo"] == nota_1.titulo
    assert response.data[1]["titulo"] == nota_2.titulo
    assert response.data[0]["autor"] == user.pk
    assert response.data[1]["autor"] == user.pk

@pytest.mark.django_db()
def test_get_nota():
    user, token = create_user()
    client.credentials(HTTP_AUTHORIZATION="")
    nota : Nota = Nota.objects.create(titulo="nota test", cuerpo="cuerpo test", autor=user)
    response = client.get(f"/api/nota/{nota.slug}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == nota.pk
    assert response.data["titulo"] == nota.titulo
    assert response.data["slug"] == nota.slug
    assert response.data["cuerpo"] == nota.cuerpo
    assert response.data["subtitulo"] == nota.subtitulo
    assert response.data["autor"] == user.pk


@pytest.mark.django_db()
def test_edit_nota():
    user, token = create_user()
    nota : Nota = Nota.objects.create(titulo="Test nota", cuerpo="Test cuerpo nota", autor=user)
    client.credentials(HTTP_AUTHORIZATION="")
    response = client.put(f"/api/nota/{nota.slug}/", data={
        "titulo":"titulo editado",
        "cuerpo":"cuerpo editado",
    }, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = client.put(f"/api/nota/{nota.slug}/", data={
        "titulo":"titulo editado",
        "cuerpo":"cuerpo editado",
    }, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == nota.pk
    assert response.data["autor"] == user.pk
    assert response.data["titulo"] == "titulo editado"
    assert response.data["cuerpo"] == "cuerpo editado"


@pytest.mark.django_db()
def test_delete_nota():
    user, token = create_user()
    nota : Nota = Nota.objects.create(titulo="Test nota", cuerpo="Test cuerpo nota", autor=user)
    client.credentials(HTTP_AUTHORIZATION="")

    response = client.delete(f"/api/nota/{nota.slug}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = client.delete(f"/api/nota/{nota.slug}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.delete(f"/api/nota/{nota.slug}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

