from rest_framework.exceptions import PermissionDenied
from users.models import User
from django.db.models.query import QuerySet
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)
from djangochannelsrestframework import permissions
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action

from .serializers import Todo, TodoSerializer
from rest_framework import status
class TodoConsumer(
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DeleteModelMixin, 
    GenericAsyncAPIConsumer,
):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self, **kwargs) -> QuerySet:
        ''' Retrive only current user todos '''
        return super().get_queryset(**kwargs).filter(user=self.scope["user"])
    
    @model_observer(Todo)
    async def todos_change_handler(self, message, observer=None, action=None, **kwargs):
        await self.send_json(dict(data=message, action=action, response_status=status.HTTP_200_OK))

    @todos_change_handler.serializer
    def todos_serializer(self, instance: Todo, action, **kwargs):
        return TodoSerializer(instance=instance).data

    @todos_change_handler.groups_for_signal
    def todos_change_handler(self, instance: Todo, **kwargs):
        yield f'-user__{instance.user_id}'
        yield f'-pk__{instance.pk}'

    @todos_change_handler.groups_for_consumer
    def todos_change_handler(self, user:int=None, todo:Todo=None, **kwargs):
        if user is not None:
            yield f'-user__{user}'

    @action()
    async def subscribe_todos_in_user(self, **kwargs):
        user:User = self.scope["user"]
        if user.is_anonymous:
            raise PermissionDenied()
        await self.todos_change_handler.subscribe(user=user.pk)
        return {}, status.HTTP_200_OK