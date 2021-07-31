from game_room.models import Room
from player.models import Player
from player.services import player_logic


def restart_game(room: "Room") -> None:
    room.update(winner=None, team_1=0, team_2=0, start=False, timer=False)


def stop_game(room: "Room") -> None:
    room.update(start=False)


def start_game(room: "Room") -> "Player":
    room.start = True
    room.save(update_fields=["start"])
    return player_logic.next_player(room)


def start_or_stop_room_timer(room: "Room", start=True) -> None:
    room.timer = start
    room.save(update_fields=["timer"])
