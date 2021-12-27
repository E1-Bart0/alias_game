from game_room.models import Room
from game_room.serializers.room import FindRoomCodeSerializer
from rest_framework import serializers
from word.models import Word


class GuessWordSerializer(FindRoomCodeSerializer):
    team = serializers.IntegerField(required=True)
    word = serializers.CharField(required=True)

    class Meta:
        model = Room
        fields = ("room_code", "host", "team", "word")

    def validate(self, attrs: dict) -> dict:
        word, room = attrs["word"], attrs["room_code"]
        word = Word.objects.filter(word=word, room=room)
        if not word.exists():
            raise serializers.ValidationError("Not such word")
        attrs["word"] = word[0]
        return attrs


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["word", "guess", "img"]
