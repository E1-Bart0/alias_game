import pytest
from game_room.models import Room
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


def test_stop_timer(user, client):
    url = reverse("new-word-stop-timer")
    room = mixer.blend(Room, host=user, room="ABCDEF", timer=True, difficulty="easy")
    data = {"room": "ABCDEF"}
    response = client.post(url, data, content_type="application/json")

    assert response.status_code == 200
    room.refresh_from_db()
    assert not room.timer


def test_get_rooms_view(client):
    url = reverse("room-list")
    rooms = mixer.cycle(2).blend(Room)
    response = client.get(url)
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 2
    assert response[0]["room"] == rooms[0].room
    assert response[1]["room"] == rooms[1].room


def test_get_room_view_if_no_room(client):
    url = reverse("room")
    response = client.get(url)
    assert response.status_code == 204


def test_get_room_view_room_exists(user, client):
    room = mixer.blend(Room, host=user)
    url = reverse("room")
    response = client.get(url)
    assert response.status_code == 200
    response = response.json()
    assert response["room"] == room.room
    assert response["difficulty"] == room.difficulty
    assert response["words_amount"] == room.words_amount
    assert response["created_at"]
    assert response["start"] == room.start
    assert response["timer"] == room.timer
    assert response["team_1"] == room.team_1
    assert response["team_2"] == room.team_2
    assert response["winner"] == room.winner
    assert response["host"] == room.host_id


def test_post_room_view(user, client):
    mixer.blend(Room, host=user)
    url = reverse("room")
    response = client.post(url)
    assert response.status_code == 201
    assert response.json() == {}


def test_create_update_room__create(client):
    url = reverse("create-update-room")
    data = {"difficulty": "easy", "words_amount": 20, "finish_time": 10}
    assert Room.objects.first() is None
    response = client.post(url, data)
    assert response.status_code == 201
    room = Room.objects.first()
    assert response.json()["room"] == room.room


def test_create_update_room__create_invalid(client):
    url = reverse("create-update-room")
    assert Room.objects.first() is None
    response = client.post(url)
    assert response.status_code == 400
    assert Room.objects.first() is None


def test_create_update_room__update__not_have_room(client):
    url = reverse("create-update-room")
    data = {"room_code": "NOT_EXISTS"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 400


def test_create_update_room__update(user, client):
    url = reverse("create-update-room")
    room = mixer.blend(
        Room,
        room="ABCDEF",
        host=user,
        words_amount=0,
        difficulty="hard",
        finish_time=10,
    )
    data = {
        "room_code": "ABCDEF",
        "words_amount": 10,
        "difficulty": "easy",
        "finish_time": 5,
    }
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    room.refresh_from_db()
    assert room.words_amount == 10
    assert room.difficulty == "easy"
    assert room.finish_time == 5


def test_create_update_room__update_if_not_all_data(user, client):
    url = reverse("create-update-room")
    room = mixer.blend(
        Room,
        host=user,
        room="ABCDEF",
        words_amount=0,
        difficulty="hard",
        finish_time=10,
    )
    data = {"room_code": "ABCDEF", "words_amount": 10}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    room.refresh_from_db()
    assert room.words_amount == 10
    assert room.difficulty == "hard"
    assert room.finish_time == 10
