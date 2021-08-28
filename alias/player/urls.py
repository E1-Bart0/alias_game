from django.urls import path
from my_auth.views import GetOrUpdateUserView

from .views import ShufflePlayersView

urlpatterns = [
    path("player", GetOrUpdateUserView.as_view(), name="user"),
    path("mix-players", ShufflePlayersView.as_view(), name="shuffle-players"),
]
