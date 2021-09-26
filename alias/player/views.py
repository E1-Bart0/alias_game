from drf_yasg.utils import swagger_auto_schema
from game_room.serializers.game import PrepareToGameSerializer
from game_room.serializers.room import FindRoomCodeSerializer
from my_auth.authentication import AuthenticationBySession
from player.serializer import PlayerUpdateSerializer
from player.services import player_logic
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class PlayerCreateUpdateView(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = FindRoomCodeSerializer
    response_serializer = PrepareToGameSerializer

    @swagger_auto_schema(
        operation_description="Update Player",
        request_body=serializer_class(),
        responses={"200": response_serializer()},
    )
    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        room = serializer.validated_data["room_code"]

        player = player_logic.update_or_create_player_for_user(
            user, room=room, is_host=(user == room.host)
        )
        data = {"room": room, "me": player, "comments": room.comments.all()}
        return Response(self.response_serializer(data).data, 200)

    @staticmethod
    @swagger_auto_schema(
        operation_description="Create Player",
        request_body=PlayerUpdateSerializer(),
        responses={"200": ""},
    )
    def post(request):
        user = request.user
        serializer = PlayerUpdateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("host")
        room = serializer.validated_data.pop("room_code")

        player_logic.update_or_create_player_for_user(
            user, room=room, **serializer.validated_data
        )
        return Response({}, status=200)


class ShufflePlayersView(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = FindRoomCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        room = serializer.validated_data.pop("room_code")
        player_logic.shuffle_players(room)
        return Response({}, status=200)
