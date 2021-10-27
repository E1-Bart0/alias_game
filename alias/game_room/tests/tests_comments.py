import pytest
from django.test.client import Client
from game_room.models import Comments, Room
from mixer.backend.django import mixer
from my_auth.models import User
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


def test_create_comment(user: User, client: Client) -> None:
    url = reverse("create-comment")
    room = mixer.blend(
        Room,
        host=user,
        room="ABCDEF",
        words_amount=0,
        difficulty="hard",
        finish_time=10,
    )

    data = {"room": "ABCDEF", "text": "Some text", "visible": 1}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 201
    comment = Comments.objects.first()

    assert comment is not None
    assert comment.room == room
    assert comment.user == user
    assert comment.text == "Some text"
    assert comment.visible == 1
