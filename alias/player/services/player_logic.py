import random

from game_room.models import Room
from my_auth.models import User
from player.models import Leader, Player


def update_or_create_player_for_user(user: "User", **kwargs) -> "Player":
    user.update(room_code=kwargs["room"].room)
    return Player.objects.update_or_create(user=user, defaults=kwargs)[0]


def shuffle_players(room: "Room"):
    players = room.in_room.all()
    team = random.sample(list(players), k=len(players) // 2)
    number = random.randint(1, 2)
    for player in players:
        if player in team:
            player.team = number
        else:
            player.team = 3 - number
        player.ready = False
        player.save(update_fields=["team", "ready"])


def next_player(room: "Room") -> "Player":
    players = room.in_room.filter(team__in=[1, 2])

    if players.filter(lead=True).count() == players.count():
        players.update(lead=False)
    team_1 = players.filter(team=1).exclude(lead=True)
    team_2 = players.filter(team=2).exclude(lead=True)

    player = max(team_1, team_2, key=lambda x: x.count()).first()
    player.lead = True
    player.save()
    leader = Leader.objects.update_or_create(room=room, defaults={"player": player})[0]
    if leader.player.team == 1:
        winner_check(room)
    return player


def winner_check(room):
    if room.team_1 >= room.words_amount or room.team_2 >= room.words_amount:
        if room.team_1 > room.team_2:
            room.winner = "Team 1"
        elif room.team_1 < room.team_2:
            room.winner = "Team 2"
        else:
            room.winner = "Tie"
        room.save(update_fields=["winner"])
