import pytest
from django.test.client import Client
from mixer.backend.django import mixer
from my_auth.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture()
def user(client: "Client") -> User:
    key = client.session.session_key
    return mixer.blend(User, host=key)
