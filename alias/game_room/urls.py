from django.urls import path
from game_room.views.comment import AddCommentView
from game_room.views.game import LeaveGameView, RestartGameView, StartStopGameView
from game_room.views.room import AllRoomListView, CreateUpdateRoom, GetOrDeleteRoomView
from player.views import PlayerCreateUpdateView

urlpatterns = [
    path("rooms", AllRoomListView.as_view(), name="room-list"),
    path("room", GetOrDeleteRoomView.as_view(), name="room"),
    path("create-room", CreateUpdateRoom.as_view(), name="create-update-room"),
    path("game", PlayerCreateUpdateView.as_view(), name="prepare-to-game"),
    path("leave-game", LeaveGameView.as_view(), name="leave-game"),
    path("create-comment", AddCommentView.as_view(), name="create-comment"),
    path("game-start", StartStopGameView.as_view(), name="start-stop-game"),
    path("restart-game", RestartGameView.as_view(), name="restart-game"),
]
