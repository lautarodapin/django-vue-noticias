
import json
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from django.conf import settings
from typing import Generator
from djangochannelsrestframework.mixins import (CreateModelMixin)
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer, AsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer

from .models import Room, Message
from .serializers import MessageSerializer, RoomSerializer

from users.models import User
from users.serializers import UserSerializer

class UserConsumerObserver(GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    async def accept(self, **kwargs):
        await super().accept(**kwargs)
        await self.model_change.subscribe()


    @model_observer(User)
    async def model_change(self, message, **kwargs):
        await self.send_json(message)


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"
    # async def accept(self, **kwargs):
    #     await super().accept(**kwargs)

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)


    # def retrieve(self, **kwargs):
    #     instance = self.get_object(**kwargs)
    #     serializer = self.get_serializer(instance=instance, action_kwargs=kwargs)
    #     return serializer.data, status.HTTP_200_OK

    def get_object(self, **kwargs) -> Room:
        return get_object_or_404(Room, pk=kwargs["pk"])

    @action()
    async def ping(self, **kwargs):
        await self.send_json("pong")

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)
        await self.notify_users()

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def create_message(self, message, **kwargs):
        room:Room = await self.get_room(pk=self.room_subscribe)
        await database_sync_to_async(Message.objects.create)(
            room=room, 
            user=self.scope["user"],
            text=message)
        return {}, 200

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)
        await self.send_json("OK")

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield 'room__%s' % instance.room_id
        yield 'pk__%s' % instance.pk

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield 'room__%s' % room

    @message_activity.serializer
    def message_activiy(self, instance:Message, action, **kwargs):
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    async def notify_users(self) -> None:
        # TODO self.groups no existe en test si es que no te subscribis a la instancia
        room:Room = await self.get_room(pk=self.room_subscribe)
        if len(self.groups) > 0:
            for group in self.groups:
                print("current users", await self.current_users(room))
                await self.channel_layer.group_send(
                    group,
                    {
                        'type':'update_users',
                        'usuarios':await self.current_users(room)
                    }
                )

    async def update_users(self, event:dict):
        await self.send(text_data=json.dumps({"data":event["usuarios"], "action":"update_users"}))
  
    @database_sync_to_async
    def get_room(self, pk:int)->Room:
        room: Room = Room.objects.get(pk=pk)
        return room

    @database_sync_to_async
    def current_users(self, room:Room):
        return [UserSerializer(usuario).data for usuario in room.current_users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room):
        user:User = self.scope["user"]
        user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user:User = self.scope["user"]
        assert user != None
        assert self.room_subscribe != None
        if not user.current_rooms.filter(pk=self.room_subscribe).exists():
            user.current_rooms.add(pk)