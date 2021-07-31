from django.db import models


class Room(models.Model):
    room = models.CharField(max_length=10, null=False, unique=True, primary_key=True)
    host = models.ForeignKey(
        "my_auth.User", related_name="my_room", on_delete=models.CASCADE
    )
    difficulty = models.CharField(max_length=20, default="easy")
    words_amount = models.IntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    start = models.BooleanField(default=False)
    timer = models.BooleanField(default=False)
    team_1 = models.IntegerField(default=0)
    team_2 = models.IntegerField(default=0)
    winner = models.CharField(max_length=10, null=True)
    finish_time = models.IntegerField(default=60)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
