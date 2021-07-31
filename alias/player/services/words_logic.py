from game_room.models import Room
from word.models import EasyWord, HardWord, MediumWord, Word

WORDS_COUNT = 7
MODELS_BY_DIFFICULTY = {"easy": EasyWord, "medium": MediumWord, "hard": HardWord}


def add_words_to_room(room: "Room") -> None:
    model = MODELS_BY_DIFFICULTY[room.difficulty]
    shuffle_words = model.objects.order_by("?")
    room_words = set(map(lambda w: w.word, room.room_words.all()))
    counter = 0
    for word in shuffle_words:
        if counter == WORDS_COUNT:
            break
        if word.word in room_words:
            continue
        Word.objects.create(word=word.word, room=room, img=word.img).save()
        counter += 1


def guess_word(room: "Room", word: "Word", team: int) -> None:
    team_name = f"team_{team}"
    setattr(room, team_name, getattr(room, team_name) + 1)
    word.guess = 1
    room.save()
    word.save()
