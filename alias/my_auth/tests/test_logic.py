import pytest
from mixer.backend.django import mixer
from my_auth.models import User
from my_auth.services.user_crud import UserLogic

pytestmark = pytest.mark.django_db


def test_update():
    user = mixer.blend(User)
    data = {"name": "New", "color": "new"}
    UserLogic.update_user(user, data)
    user.refresh_from_db()
    assert user.name == "New"
    assert user.color == "new"
