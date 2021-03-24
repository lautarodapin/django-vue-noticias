from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError
class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "date_joined", "last_login", "token", "password"]
        extra_kwargs = {
            "password":{
                "write_only":True, 
                "required":True
            }
        }

    def get_token(self, obj:User):
        return obj.auth_token.key

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

    def validate_password(self, value):
        user = self.context["request"].user
        validate_password(password=value, user=user)

