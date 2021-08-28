from django.urls import path
from .views import GetOrUpdateUserView

urlpatterns = [
    path("player", GetOrUpdateUserView.as_view(), name="user"),
]
