from typing import Any

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.request import Request


def index(request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
    return render(request, "frontend/index.html")
