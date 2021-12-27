import pytest
from django.test.client import Client
from game_room.models import Room
from mixer.backend.django import mixer
from my_auth.models import User
from rest_framework.reverse import reverse
from word.models import EasyWord, Word

pytestmark = pytest.mark.django_db


def test_new_words(user: User, client: Client) -> None:
    url = reverse("new-word-stop-timer")
    room = mixer.blend(Room, host=user, room="ABCDEF", timer=False, difficulty="easy")
    mixer.cycle(50).blend(EasyWord)

    data = {"room": "ABCDEF"}
    response = client.patch(url, data, content_type="application/json")

    assert response.status_code == 200
    room.refresh_from_db()
    assert room.timer


def test_guess_word(user: User, client: Client) -> None:
    url = reverse("guess-word")
    room = mixer.blend(Room, host=user, room="ABCDEF", difficulty="easy")
    team_1_score = room.team_1
    team_2_score = room.team_2
    word = mixer.blend(Word, word="Guessed Word", room=room)
    data = {"room_code": "ABCDEF", "word": "Guessed Word", "team": 1}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200

    word.refresh_from_db()
    room.refresh_from_db()
    assert word.guess == 1
    assert room.team_1 == team_1_score + 1
    assert room.team_2 == team_2_score
