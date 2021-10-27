from drf_yasg.utils import swagger_auto_schema
from game_room.models import Room
from game_room.serializers.room import RoomNameSerializer
from game_room.services import game_logic
from my_auth.authentication import AuthenticationBySession
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from word.serializers import GuessWordSerializer
from word.services import words_logic


class NewWordStopTimerView(APIView):
    authentication_classes = [AuthenticationBySession]

    @staticmethod
    @swagger_auto_schema(
        operation_description="Start Timer",
        request_body=RoomNameSerializer(),
        responses={"200": ""},
    )
    def patch(request: Request) -> Response:
        room = get_object_or_404(Room, room=request.data.get("room"))
        game_logic.start_or_stop_room_timer(room, start=True)
        words_logic.add_words_to_room(room)
        return Response({}, status=200)

    @staticmethod
    @swagger_auto_schema(
        operation_description="Stop Timer",
        request_body=RoomNameSerializer(),
        responses={"200": ""},
    )
    def post(request: Request) -> Response:
        room = get_object_or_404(Room, room=request.data.get("room"))
        game_logic.start_or_stop_room_timer(room, start=False)
        return Response({}, status=200)


class GuessWordView(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = GuessWordSerializer

    @swagger_auto_schema(
        operation_description="Change Word to Guessed",
        request_body=serializer_class(),
        responses={"200": ""},
    )
    def patch(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data.get("room_code")
        word = serializer.validated_data.get("word")
        team = serializer.validated_data.get("team")
        words_logic.guess_word(room, word, team)
        return Response({}, status=200)
