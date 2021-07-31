from game_room.models import Room
from game_room.services import game_logic
from my_auth.authentication import AuthenticationBySession
from player.services import words_logic
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from word.serializers import GuessWordSerializer


class NewWordStopTimerView(APIView):
    authentication_classes = [AuthenticationBySession]

    @staticmethod
    def patch(request):
        room = get_object_or_404(Room, room=request.data.get("room"))
        game_logic.start_or_stop_room_timer(room, start=True)
        words_logic.add_words_to_room(room)
        return Response({}, status=200)

    @staticmethod
    def post(request):
        room = get_object_or_404(Room, room=request.data.get("room"))
        game_logic.start_or_stop_room_timer(room, start=False)
        return Response({}, status=200)


class GuessWordView(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = GuessWordSerializer

    def patch(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data.get("room_code")
        word = serializer.validated_data.get("word")
        team = serializer.validated_data.get("team")
        words_logic.guess_word(room, word, team)
        return Response({}, status=200)
