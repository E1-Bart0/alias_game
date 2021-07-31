import pytest
from game_room.models import Room
from mixer.backend.django import mixer
from player.models import Leader, Player
from player.services.player_logic import next_player

pytestmark = pytest.mark.django_db


def test_next_player__if_teams_are_same_and_no_leader(user):
    room = mixer.blend(Room, host=user)

    team_1_host = mixer.blend(Player, room=room, user=user, team=1, lead=False)
    team_1_player_1 = mixer.blend(Player, room=room, team=1, lead=False)

    team_2_player_1 = mixer.blend(Player, room=room, team=2, lead=False)
    team_2_player_2 = mixer.blend(Player, room=room, team=2, lead=False)

    room.refresh_from_db()
    result = next_player(room)
    leader = Leader.objects.first()

    team_1_host.refresh_from_db()
    team_1_player_1.refresh_from_db()
    team_2_player_1.refresh_from_db()
    team_2_player_2.refresh_from_db()

    assert room.in_room.count() == 4
    assert result == team_1_host
    assert leader.room == room
    assert leader.player == team_1_host
    assert team_1_host.lead
    assert not team_1_player_1.lead
    assert not team_2_player_1.lead
    assert not team_2_player_2.lead


def test_next_player__if_team_2_is_gt_team_1_and_no_leader(user):
    room = mixer.blend(Room, host=user)
    team_1_host = mixer.blend(Player, room=room, user=user, team=1, lead=False)
    team_2_player_1 = mixer.blend(Player, room=room, team=2, lead=False)
    team_2_player_2 = mixer.blend(Player, room=room, team=2, lead=False)

    room.refresh_from_db()
    result = next_player(room)
    leader = Leader.objects.first()

    team_1_host.refresh_from_db()
    team_2_player_1.refresh_from_db()
    team_2_player_2.refresh_from_db()

    assert room.in_room.count() == 3
    assert result == team_2_player_1
    assert leader.room == room
    assert leader.player == team_2_player_1
    assert not team_1_host.lead
    assert team_2_player_1.lead
    assert not team_2_player_2.lead


def test_next_player__if_team_1_is_gt_team_2_and_no_leader(user):
    room = mixer.blend(Room, host=user)
    team_1_host = mixer.blend(Player, room=room, user=user, team=1, lead=False)
    team_1_player_2 = mixer.blend(Player, room=room, team=1, lead=False)
    team_2_player_2 = mixer.blend(Player, room=room, team=2, lead=False)

    room.refresh_from_db()
    result = next_player(room)
    leader = Leader.objects.first()

    team_1_host.refresh_from_db()
    team_1_player_2.refresh_from_db()
    team_2_player_2.refresh_from_db()

    assert room.in_room.count() == 3
    assert result == team_1_host
    assert leader.room == room
    assert leader.player == team_1_host
    assert team_1_host.lead
    assert not team_1_player_2.lead
    assert not team_2_player_2.lead


def test_next_player__if_team_2_is_gt_team_1_and_leader_was_team_2_player(user):
    room = mixer.blend(Room, host=user)
    team_1_host = mixer.blend(Player, room=room, user=user, team=1, lead=False)
    team_2_player_1 = mixer.blend(Player, room=room, team=2, lead=True)
    team_2_player_2 = mixer.blend(Player, room=room, team=2, lead=False)

    room.refresh_from_db()
    result = next_player(room)
    leader = Leader.objects.first()

    team_1_host.refresh_from_db()
    team_2_player_1.refresh_from_db()
    team_2_player_2.refresh_from_db()

    assert room.in_room.count() == 3
    assert result == team_1_host
    assert leader.room == room
    assert leader.player == team_1_host
    assert team_1_host.lead
    assert team_2_player_1.lead
    assert not team_2_player_2.lead


def test_next_player__if_all_leads_in_team1(user):
    room = mixer.blend(Room, host=user)
    team_1_host = mixer.blend(Player, room=room, user=user, team=1, lead=True)
    team_1_player_1 = mixer.blend(Player, room=room, team=1, lead=True)
    team_2_player_1 = mixer.blend(Player, room=room, team=2, lead=True)
    team_2_player_2 = mixer.blend(Player, room=room, team=2, lead=False)

    room.refresh_from_db()
    result = next_player(room)
    leader = Leader.objects.first()

    team_1_host.refresh_from_db()
    team_1_player_1.refresh_from_db()
    team_2_player_1.refresh_from_db()
    team_2_player_2.refresh_from_db()

    assert room.in_room.count() == 4
    assert result == team_2_player_2
    assert leader.room == room
    assert leader.player == team_2_player_2
    assert team_1_host.lead
    assert team_1_player_1.lead
    assert team_2_player_1.lead
    assert team_2_player_2.lead


def test_next_player__if_all_leads(user):
    room = mixer.blend(Room, host=user)
    team_1_host = mixer.blend(Player, room=room, user=user, team=1, lead=True)
    team_1_player_1 = mixer.blend(Player, room=room, team=1, lead=True)
    team_2_player_1 = mixer.blend(Player, room=room, team=2, lead=True)
    team_2_player_2 = mixer.blend(Player, room=room, team=2, lead=True)

    room.refresh_from_db()
    result = next_player(room)
    leader = Leader.objects.first()

    team_1_host.refresh_from_db()
    team_1_player_1.refresh_from_db()
    team_2_player_1.refresh_from_db()
    team_2_player_2.refresh_from_db()

    assert room.in_room.count() == 4
    assert result == team_1_host
    assert leader.room == room
    assert leader.player == team_1_host
    assert team_1_host.lead
    assert not team_1_player_1.lead
    assert not team_2_player_1.lead
    assert not team_2_player_2.lead
