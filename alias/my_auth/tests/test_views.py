import pytest
from django.test.client import Client
from my_auth.models import User
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


def test_get_player_view_create_new_user(client: Client) -> None:
    url = reverse("user")
    assert not User.objects.count()
    response = client.get(url)
    assert response.status_code == 200
    assert User.objects.count() == 1
    user = User.objects.first()
    response = response.json()
    assert user is not None
    assert response["id"] == user.id
    assert response["host"] == user.host
    assert response["name"] == user.name
    assert response["color"] == user.color
    assert response["room_code"] == user.room_code


def test_get_player_view_user_already_exists(client: Client) -> None:
    url = reverse("user")
    assert not User.objects.count()

    response = client.get(url)
    assert response.status_code == 200
    assert User.objects.count() == 1

    response = client.get(url)
    assert response.status_code == 200
    assert User.objects.count() == 1


def test_get_player_patch(client: Client) -> None:
    url = reverse("user")
    data = {"name": "Me", "color": "#000"}
    response = client.patch(url, data=data, content_type="application/json")
    assert response.status_code == 200
    user = User.objects.first()
    assert user is not None
    assert user.name == "Me"
    assert user.color == "#000"

    response = response.json()
    assert response["id"] == user.id
    assert response["host"] == user.host
    assert response["name"] == "Me"
    assert response["color"] == "#000"
    assert response["room_code"] == user.room_code
