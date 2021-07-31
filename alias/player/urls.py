"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from game_room.views.comment import AddCommentView
from game_room.views.game import LeaveGameView, RestartGameView, StartStopGameView
from game_room.views.room import AllRoomListView, CreateUpdateRoom, GetOrDeleteRoomView
from my_auth.views import GetOrUpdateUserView
from player.views import PlayerCreateUpdateView, ShufflePlayersView
from word.views import GuessWordView, NewWordStopTimerView

urlpatterns = [
    path("player", GetOrUpdateUserView.as_view(), name="user"),
    path("rooms", AllRoomListView.as_view(), name="room-list"),
    path("room", GetOrDeleteRoomView.as_view(), name="room"),
    path("create-room", CreateUpdateRoom.as_view(), name="create-update-room"),
    path("game", PlayerCreateUpdateView.as_view(), name="prepare-to-game"),
    path("leave-game", LeaveGameView.as_view(), name="leave-game"),
    path("create-comment", AddCommentView.as_view(), name="create-comment"),
    path("game-start", StartStopGameView.as_view(), name="start-stop-game"),
    path("new-word", NewWordStopTimerView.as_view(), name="new-word-stop-timer"),
    path("guess-word", GuessWordView.as_view(), name="guess-word"),
    path("restart-game", RestartGameView.as_view(), name="restart-game"),
    path("mix-players", ShufflePlayersView.as_view(), name="shuffle-players"),
]
