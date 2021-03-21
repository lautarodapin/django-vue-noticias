from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Todo
from django.contrib.humanize.templatetags.humanize import naturaltime
class TodoSerializer(serializers.ModelSerializer):
    time_since_created = serializers.SerializerMethodField()
    time_since_last_mod = serializers.SerializerMethodField()
    class Meta:
        model = Todo
        fields = [
            "id",
            "created_at",
            "mod_at",
            "user",
            "title",
            "is_done",
            "time_since_created",
            "time_since_last_mod",
        ]

    def to_representation(self, instance: Todo):
        representation = super().to_representation(instance)
        representation["user"] = UserSerializer(instance.user).data
        return representation

    def get_time_since_created(self, obj: Todo):
        return str(naturaltime(obj.created_at))

    def get_time_since_last_mod(self, obj: Todo):
        return str(naturaltime(obj.mod_at))

