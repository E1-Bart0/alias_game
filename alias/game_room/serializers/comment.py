from game_room.models import Comments
from my_auth.serializers import MiniUserSerializer
from rest_framework import serializers


class CreateCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comments
        fields = ["room", "user", "visible", "text"]


class CommentsSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(required=True)

    class Meta:
        model = Comments
        fields = ["user", "visible", "text"]
