from my_auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "host", "created_at", "name", "color", "room_code")


class UserUpdateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ["color", "name"]


class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "color", "id"]
