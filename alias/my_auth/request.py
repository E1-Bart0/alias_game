from my_auth.models import User
from rest_framework.request import Request


class AuthenticatedRequest(Request):
    user: User
