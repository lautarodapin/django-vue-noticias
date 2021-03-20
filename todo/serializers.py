from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Todo
        fields = ["id", "created_at", "mod_at", "user", "title", "is_done"]

    def to_representation(self, instance: Todo):
        representation = super().to_representation(instance)
        representation["user"] = UserSerializer(instance.user).data
        return representation