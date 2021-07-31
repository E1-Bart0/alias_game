from django.db import models


class Player(models.Model):
    user = models.OneToOneField(
        "my_auth.User", related_name="player", on_delete=models.CASCADE
    )
    team = models.IntegerField(default=0)
    ready = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    room = models.ForeignKey(
        "game_room.Room", related_name="in_room", on_delete=models.CASCADE
    )
    lead = models.BooleanField(default=False)


class Leader(models.Model):
    room = models.ForeignKey(
        "game_room.Room", related_name="room_lead", on_delete=models.CASCADE
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
