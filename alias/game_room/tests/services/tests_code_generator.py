from unittest.mock import patch

import pytest
from game_room.models import Room
from game_room.services.room_logic import generate_unique_code
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


@patch("random.choices")
def test_code_generator_if_room_not_found(mock):
    mock.return_value = ["A", "B", "C", "D", "E", "F"]
    code = generate_unique_code()
    assert code == "ABCDEF"


@patch("random.choices")
def test_code_generator_if_such_room_exists(mock):
    mock.side_effect = (
        ["E", "X", "I", "S", "T", "S"],
        ["N", "O", "T", "E", "X", "I", "S", "T", "S"],
    )
    mixer.blend(Room, name="EXISTS")
    code = generate_unique_code()
    assert "NOTEXISTS"
    assert isinstance(code, str)
