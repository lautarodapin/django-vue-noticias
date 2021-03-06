from django.db.models import QuerySet
from rest_framework import status, viewsets, views
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

from news.models import (Nota, Comentario)
from news.serializers import (NotaSerializer, ComentarioSerializer)

from chat.models import (Message, Room,)
from chat.serializers import (MessageSerializer, RoomSerializer,)

from users.models import User
from users.serializers import UserSerializer

from todo.serializers import (Todo, TodoSerializer,)

from rest_framework.response import Response
from typing import List
import json

class TodoViewset(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly,]
class ExtendedObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response:Response = super().post(request, *args, **kwargs)
        response.data["user"] = UserSerializer(Token.objects.get(key=response.data["token"]).user).data
        return response

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], url_path="get-user-with-token", permission_classes=[AllowAny])
    def get_user_with_token(self, request):
        user = User.objects.get(auth_token__key=request.query_params['token'])
        return Response({"user":UserSerializer(user).data}, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all().order_by('-created_at')
    serializer_class = NotaSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer:NotaSerializer):
        return super().perform_create(serializer)

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly,]




class LoginView(views.APIView):

    def get(self, request, format=None):
        return Response({"details":"Only post allowed"})

    def post(self, request, format=None):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            return Response({
                "errors": {
                    "__all__": "Please enter both username and password"
                }
            }, status=400)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Success"})
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST,
        )

@ensure_csrf_cookie
@api_view(["GET",])
def set_csrf_token(request):
    """
    This will be `/api/set-csrf-cookie/` on `urls.py`
    """
    return Response({"details": "CSRF cookie set"}, status=status.HTTP_200_OK)


@api_view(["POST",])
def obtain_token(request):
    if  request.user.is_authenticated:
        return Response({
            "user":UserSerializer(instance=request.user).data, 
            "token":request.user.auth_token.key
        }, status=status.HTTP_200_OK)
    return Response({"detail":"Forbidden"}, status=status.HTTP_403_FORBIDDEN)