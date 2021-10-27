from django.db import models

IMG = "https://pixabay.com/get/g4b09d9e0d046b094964dc9977fdc17ef984ffc0a09a6b0f4947ab5bff0448dfe1e40a4a4c3fed4d594931b0d4c5d0f5b2b17e7561f3f44e90845bc30eca2df21_640.jpg"


class AbstractWord(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(null=False, max_length=255, unique=True)
    img = models.CharField(default=IMG, max_length=255)

    def __str__(self) -> str:
        return str(self.word)

    class Meta:
        abstract = True


class EasyWord(AbstractWord):
    pass


class MediumWord(AbstractWord):
    pass


class HardWord(AbstractWord):
    pass


class Word(AbstractWord):
    room = models.ForeignKey(
        "game_room.Room", related_name="room_words", on_delete=models.CASCADE
    )
    guess = models.IntegerField(default=0)
