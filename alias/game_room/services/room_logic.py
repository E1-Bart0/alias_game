import random
import string

from game_room.models import Room
from my_auth.models import User


def delete_prev_room(user: "User") -> None:
    rooms = user.my_room.all()
    for room in rooms:
        User.objects.filter(room_code=room.room).update(room_code=None)
    rooms.delete()


def leave_member_from_room(user: "User", room: "Room") -> None:
    user.update(room_code=None)
    if user == room.host:
        delete_prev_room(user)
    else:
        user.player.delete()
        room.start = False
        room.save()


def create_new_room(user: "User", data: dict) -> Room:
    delete_prev_room(user)
    room_name = generate_unique_code()
    return Room.objects.create(room=room_name, host=user, **data)


def update_room(room: "Room", data: dict) -> None:
    for key, value in data.items():
        setattr(room, key, value)
    room.save()


def generate_unique_code() -> str:
    length = 6
    code = "".join(random.choices(string.ascii_uppercase, k=length))
    while Room.objects.filter(room=code).exists():
        code = "".join(random.choices(string.ascii_uppercase, k=length))
    return code
