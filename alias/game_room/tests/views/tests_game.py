import pytest
from django.test.client import Client
from game_room.models import Comments, Room
from mixer.backend.django import mixer
from my_auth.models import User
from player.models import Leader, Player
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


def test_restart_game(user: User, client: Client) -> None:
    url = reverse("restart-game")
    room = mixer.blend(
        Room,
        host=user,
        room="ABCDEF",
        winner="win",
        team_1=1,
        team_2=2,
        start=True,
        timer=True,
    )

    data = {"room_code": "ABCDEF"}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    room.refresh_from_db()
    assert room.winner is None
    assert room.team_1 == 0
    assert room.team_2 == 0
    assert not room.start
    assert not room.timer


def test_start_game(user: User, client: Client) -> None:
    url = reverse("start-stop-game")
    room = mixer.blend(
        Room,
        host=user,
        room="ABCDEF",
        words_amount=0,
        difficulty="hard",
        finish_time=10,
    )
    player = mixer.blend(Player, user=user, room=room, lead=False, team=1)

    data = {"room": "ABCDEF"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    response_json = response.json()

    room.refresh_from_db()
    player.refresh_from_db()

    assert room.start
    leader = Leader.objects.first()
    assert leader is not None
    assert leader.player == player
    assert leader.room == room
    assert player.lead
    assert response_json["user"]["name"] == user.name
    assert response_json["team"] == player.team
    assert response_json["lead"] == player.lead
    assert response_json["ready"] == player.ready
    assert response_json["is_host"] == player.is_host


def test_stop_game(user: User, client: Client) -> None:
    url = reverse("start-stop-game")
    room = mixer.blend(Room, host=user, room="ABCDEF", start=True)

    data = {"room": "ABCDEF"}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    room.refresh_from_db()
    assert not room.start


def test_prepare_to_game_view__patch(user: User, client: Client) -> None:
    url = reverse("prepare-to-game")
    room = mixer.blend(
        Room,
        host=user,
        room="ABCDEF",
        words_amount=0,
        difficulty="hard",
        finish_time=10,
    )
    mixer.cycle(2).blend(Comments, room=room)
    data = {"room_code": "ABCDEF", "words_amount": 10}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["room"]["room"] == room.room
    assert response_json["room"]["difficulty"] == room.difficulty
    assert response_json["room"]["start"] == room.start
    assert response_json["room"]["timer"] == room.timer
    assert response_json["room"]["team_1"] == room.team_1
    assert response_json["room"]["team_2"] == room.team_2
    assert response_json["room"]["words_amount"] == room.words_amount
    assert response_json["room"]["winner"] == room.winner
    assert response_json["room"]["finish_time"] == room.finish_time
    assert response_json["room"]["room_words"] == []
    assert response_json["room"]["room_lead"] == []
    assert len(response_json["room"]["in_room"]) == 1
    assert response_json["room"]["in_room"][0]["user"]["name"] == user.name
    assert response_json["me"]["user"]["name"] == user.name
    assert response_json["me"]["team"] == user.player.team
    assert response_json["me"]["ready"] == user.player.ready
    assert response_json["me"]["is_host"] == user.player.is_host
    assert response_json["me"]["lead"] == user.player.lead
    assert len(response_json["comments"]) == 2


def test_prepare_to_game_view__post(user: User, client: Client) -> None:
    url = reverse("prepare-to-game")
    room = mixer.blend(
        Room,
        host=user,
        room="ABCDEF",
        words_amount=0,
        difficulty="hard",
        finish_time=10,
    )
    mixer.blend(Player, user=user, room=room, team=0, ready=False)

    data = {"room_code": "ABCDEF", "team": 1, "ready": True}
    response = client.post(url, data, content_type="application/json")
    user.player.refresh_from_db()
    assert response.status_code == 200
    assert user.player.team == 1
    assert user.player.ready


def test_leave_game__post(user: User, client: Client) -> None:
    url = reverse("leave-game")
    room = mixer.blend(
        Room,
        host=user,
        room="ABCDEF",
        words_amount=0,
        difficulty="hard",
        finish_time=10,
    )
    mixer.blend(Player, user=user, room=room, team=0, ready=False)

    data = {"room_code": "ABCDEF"}
    response = client.post(url, data, content_type="application/json")
    user.refresh_from_db()
    assert response.status_code == 200
    assert Player.objects.count() == 0
    assert Room.objects.count() == 0
    assert user.room_code is None
