from django.db import models


class Comments(models.Model):
    user = models.ForeignKey("my_auth.User", on_delete=models.CASCADE)
    room = models.ForeignKey(
        "game_room.Room", related_name="comments", on_delete=models.CASCADE
    )
    visible = models.IntegerField(default=0)
    text = models.CharField(null=False, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
