import uuid

from my_auth.models import User
from rest_framework.authentication import BaseAuthentication


class AuthenticationBySession(BaseAuthentication):
    """Authentication by token"""

    def authenticate(self, request):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        host = request.session.session_key
        return User.objects.get_or_create(
            host=host, defaults={"username": uuid.uuid4()}
        )
