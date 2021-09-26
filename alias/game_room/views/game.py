from drf_yasg.utils import swagger_auto_schema
from game_room.models import Room
from game_room.serializers.room import (
    FindRoomCodeSerializer,
    FindRoomSerializer,
    RoomNameSerializer,
)
from game_room.services import game_logic, room_logic
from my_auth.authentication import AuthenticationBySession
from player.serializer import PlayerSerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


class LeaveGameView(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = FindRoomCodeSerializer

    @swagger_auto_schema(
        operation_description="Leave From Room",
        request_body=serializer_class(),
        responses={"200": ""},
    )
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        room = serializer.validated_data.pop("room_code")

        room_logic.leave_member_from_room(user, room)
        return Response({}, status=status.HTTP_200_OK)


class StartStopGameView(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = FindRoomSerializer
    serializer = PlayerSerializer

    @swagger_auto_schema(
        operation_description="Start Game",
        request_body=serializer_class(),
        responses={"200": serializer_class()},
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.validated_data.pop("room")

        player = game_logic.start_game(room)
        return Response(self.serializer(player).data, status=200)

    @staticmethod
    @swagger_auto_schema(
        operation_description="Stop Game",
        request_body=RoomNameSerializer(),
        responses={"200": ""},
    )
    def post(request):
        room = get_object_or_404(Room, room=request.data.get("room"))
        game_logic.stop_game(room)
        return Response({}, status=200)


class RestartGameView(APIView):
    authentication_classes = [AuthenticationBySession]

    @staticmethod
    @swagger_auto_schema(
        operation_description="Restart Game",
        request_body=RoomNameSerializer(),
        responses={"200": ""},
    )
    def post(request):
        room = get_object_or_404(Room, room=request.data.get("room_code"))
        game_logic.restart_game(room)
        return Response({}, status=200)
