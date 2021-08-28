from django.urls import path
from .views import GuessWordView, NewWordStopTimerView

urlpatterns = [
    path("new-word", NewWordStopTimerView.as_view(), name="new-word-stop-timer"),
    path("guess-word", GuessWordView.as_view(), name="guess-word"),
]
