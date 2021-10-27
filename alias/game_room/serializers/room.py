from game_room.models import Room
from rest_framework import serializers


class CreateRoomSerializer(serializers.ModelSerializer):
    difficulty = serializers.CharField(required=True)

    class Meta:
        model = Room
        fields = ("difficulty", "words_amount", "finish_time")


class RoomNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("room",)


class FindRoomSerializer(serializers.Serializer):
    room = serializers.SlugRelatedField(
        required=True, queryset=Room.objects.all(), slug_field="room"
    )


class FindRoomCodeSerializer(serializers.ModelSerializer):
    room_code = serializers.SlugRelatedField(
        required=True, queryset=Room.objects.all(), slug_field="room"
    )
    host = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Room
        fields = ("room_code", "host")


class UpdateRoomSerializer(FindRoomCodeSerializer):
    def validate(self, attrs: dict) -> dict:
        if attrs["room_code"].host != attrs["host"]:
            raise serializers.ValidationError("Can't change not your own room")
        return attrs

    class Meta:
        model = Room
        fields = ("room_code", "host", "words_amount", "difficulty", "finish_time")


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
