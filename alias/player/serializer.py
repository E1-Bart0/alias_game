from game_room.models import Room
from game_room.serializers.room import FindRoomCodeSerializer
from my_auth.serializers import MiniUserSerializer
from player.models import Leader, Player
from rest_framework import serializers


class PlayerUpdateSerializer(FindRoomCodeSerializer):
    team = serializers.IntegerField(required=True)
    ready = serializers.BooleanField(required=True)

    class Meta:
        model = Room
        fields = ("room_code", "host", "team", "ready")


class PlayerSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(required=True)

    class Meta:
        model = Player
        fields = ["user", "team", "ready", "is_host", "lead"]


class LeaderSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(required=True)

    class Meta:
        model = Leader
        fields = ["player"]
