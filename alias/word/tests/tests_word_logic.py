import pytest
from game_room.models import Room
from mixer.backend.django import mixer
from player.services import words_logic
from player.services.words_logic import WORDS_COUNT
from word.models import EasyWord

pytestmark = pytest.mark.django_db


def test_words_logic__add_words_to_room(user):
    room = mixer.blend(Room, host=user)
    mixer.cycle(50).blend(EasyWord)

    words_logic.add_words_to_room(room)
    room.refresh_from_db()
    assert room.room_words.count() == WORDS_COUNT
