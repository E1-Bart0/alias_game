import pytest
from game_room.models import Room
from game_room.services.room_logic import delete_prev_room
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


def test_delete_prev_room_room_do_not_exists(user):
    delete_prev_room(user)
    assert user.my_room.count() == 0


def test_delete_prev_room_room_exists(user):
    mixer.blend(Room, host=user)
    assert user.my_room.count() == 1
    delete_prev_room(user)
    assert user.my_room.count() == 0
