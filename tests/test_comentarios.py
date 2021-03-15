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
def test_login_required_for_creating_comentario():
    user, token = create_user()
    nota : Nota = Nota.objects.create(titulo="test nota", autor=user)

    response = client.post("/api/comentario/", data={
        "cuerpo":"test comentario",
        "nota":nota.slug,
    }, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db()
def test_create_comentario():
    user, token = create_user()
    nota : Nota = Nota.objects.create(titulo="test nota", autor=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    response = client.post("/api/comentario/", data=dict(
        cuerpo="comentario test",
        nota=nota.slug,
    ))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["cuerpo"] == "comentario test"
    assert response.data["nota"]["id"] == nota.pk
    assert response.data["autor"]["id"] == user.pk


@pytest.mark.django_db()
def test_get_comentarios():
    user, token = create_user()
    nota : Nota = Nota.objects.create(titulo="test nota", autor=user)
    client.credentials(HTTP_AUTHORIZATION="")

    comentario_1 = Comentario.objects.create(cuerpo="comentario 1", autor=user, nota=nota)
    comentario_2 = Comentario.objects.create(cuerpo="comentario 2", autor=user, nota=nota)

    response = client.get("/api/comentario/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data.__len__() == 2
    assert response.data[0]["id"] == comentario_1.pk
    assert response.data[0]["cuerpo"] == comentario_1.cuerpo
    assert response.data[0]["autor"]["id"] == comentario_1.autor.pk
    assert response.data[0]["nota"]["id"] == comentario_1.nota.pk
    assert response.data[1]["id"] == comentario_2.pk
    assert response.data[1]["cuerpo"] == comentario_2.cuerpo
    assert response.data[1]["autor"]["id"] == comentario_2.autor.pk
    assert response.data[1]["nota"]["id"] == comentario_2.nota.pk



@pytest.mark.django_db()
def test_get_comentario():
    user, token = create_user()
    nota : Nota = Nota.objects.create(titulo="test nota", autor=user)
    client.credentials(HTTP_AUTHORIZATION="")

    comentario = Comentario.objects.create(cuerpo="comentario 1", autor=user, nota=nota)

    response = client.get(f"/api/comentario/{comentario.pk}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == comentario.pk
    assert response.data["cuerpo"] == comentario.cuerpo
    assert response.data["autor"]["id"] == comentario.autor.pk
    assert response.data["nota"]["id"] == comentario.nota.pk

@pytest.mark.django_db()
def test_edit_comentario():
    user, token = create_user()
    nota : Nota = Nota.objects.create(titulo="test nota", autor=user)
    comentario = Comentario.objects.create(cuerpo="comentario 1", autor=user, nota=nota)
    client.credentials(HTTP_AUTHORIZATION="")
    response = client.put(f"/api/comentario/{comentario.pk}/", data=dict(
        cuerpo="comentario editado"
    ))
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.put(f"/api/comentario/{comentario.pk}/", data=dict(
        cuerpo="comentario editado"
    ))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == comentario.pk
    assert response.data["cuerpo"] == "comentario editado"
    assert response.data["autor"]["id"] == comentario.autor.pk
    assert response.data["nota"]["id"] == comentario.nota.pk

@pytest.mark.django_db()
def test_delete_comentario():
    user, token = create_user()
    nota : Nota = Nota.objects.create(titulo="test nota", autor=user)
    comentario = Comentario.objects.create(cuerpo="comentario 1", autor=user, nota=nota)
    client.credentials(HTTP_AUTHORIZATION="")
    response = client.delete(f"/api/comentario/{comentario.pk}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.delete(f"/api/comentario/{comentario.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/api/comentario/{comentario.pk}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND