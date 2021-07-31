from game_room.models import Room
from game_room.serializers.room import (
    CreateRoomSerializer,
    RoomNameSerializer,
    RoomsSerializer,
    UpdateRoomSerializer,
)
from game_room.services import room_logic
from my_auth.authentication import AuthenticationBySession
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView


class AllRoomListView(generics.ListAPIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = RoomsSerializer
    queryset = Room.objects.all()


class GetOrDeleteRoomView(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = RoomsSerializer

    def get(self, request):
        host_room = request.user.my_room.first()
        if host_room is None:
            return Response({}, status=204)
        return Response(
            self.serializer_class(host_room).data, status=status.HTTP_200_OK
        )

    @staticmethod
    def post(request):
        room_logic.delete_prev_room(request.user)
        return Response({}, status=201)


class CreateUpdateRoom(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer = CreateRoomSerializer
    response_serializer = RoomNameSerializer

    def post(self, request):
        user = request.user
        room_serializer = self.serializer(data=request.data)
        room_serializer.is_valid(raise_exception=True)

        room = room_logic.create_new_room(user, room_serializer.validated_data)
        return Response(self.response_serializer(room).data, status=201)

    @staticmethod
    def patch(request):
        serializer = UpdateRoomSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data.pop("room_code")
        serializer.validated_data.pop("host")
        room_logic.update_room(room, serializer.validated_data)
        return Response({}, status=200)
