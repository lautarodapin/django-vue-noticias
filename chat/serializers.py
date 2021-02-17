from .models import *
from users.models import User
from rest_framework import serializers
from users.serializers import UserSerializer

class RoomSerializerField(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = []
        # read_only_fields = ["code", "host", "slug", "current_users", "nombre"]

class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user_extra = UserSerializer(source="user", read_only=True)
    room_extra = RoomSerializerField(source="room", read_only=True)
    class Meta:
        model = Message
        fields = ["id", "created_at_formatted", "room", "text", "user", "user_extra", "room_extra"]

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ["pk", "code", "nombre", "host", "slug", "messages", "current_users", "last_message"]
        depth = 1
        read_only_fields = ["code", "slug", "messages", "last_message"]
        
    def get_last_message(self, obj:Room):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data


        