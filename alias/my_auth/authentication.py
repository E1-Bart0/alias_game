import uuid
from typing import Tuple

from my_auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request


class AuthenticationBySession(BaseAuthentication):
    """Authentication by token"""

    def authenticate(self, request: Request) -> Tuple[User, bool]:
        if not request.session.exists(request.session.session_key):
            request.session.create()
        host = request.session.session_key
        return User.objects.get_or_create(
            host=host, defaults={"username": uuid.uuid4()}
        )
