import pytest
from game_room.models import Room
from mixer.backend.django import mixer
from player.models import Player
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


def test_shuffle_players(user, client):
    url = reverse("shuffle-players")
    room = mixer.blend(Room, host=user, room="ABCDEF")
    mixer.cycle(6).blend(Player, room=room)

    data = {"room_code": "ABCDEF"}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    assert Player.objects.filter(team=1).count() == 3
    assert Player.objects.filter(team=2).count() == 3
