from game_room.models import Room
from game_room.serializers.comment import CommentsSerializer
from player.serializer import LeaderSerializer, PlayerSerializer
from rest_framework import serializers
from word.serializers import WordsSerializer


class GameRoomSerializer(serializers.ModelSerializer):
    in_room = PlayerSerializer(many=True, read_only=True)
    room_lead = LeaderSerializer(many=True, read_only=True)
    room_words = WordsSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "room",
            "difficulty",
            "in_room",
            "start",
            "room_lead",
            "timer",
            "room_words",
            "team_1",
            "team_2",
            "words_amount",
            "winner",
            "finish_time",
        )


class PrepareToGameSerializer(serializers.Serializer):
    room = GameRoomSerializer(required=True)
    me = PlayerSerializer(required=True)
    comments = CommentsSerializer(required=True, many=True)
