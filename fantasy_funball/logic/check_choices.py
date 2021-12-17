"""At midnight of deadline day, checks if all players have made a choice
If they haven't, Steve them"""
import json
from datetime import date, datetime, timedelta
from typing import List

import django
import pytz
import requests

from fantasy_funball.fpl_interface.interface import FPLInterface
from fantasy_funball.logic.determine_gameweek import determine_gameweek_no
from fantasy_funball.logic.random_generator import get_random_player, get_random_team

django.setup()

import logging

from fantasy_funball.models import (
    Choices,
    Fixture,
    Funballer,
    Gameday,
    Gameweek,
    Player,
)

logger = logging.getLogger("papertrail")


def is_deadline_day(gameweek_no: int) -> bool:
    """Checks if today is gameweek deadline day"""
    logger.info("Checking if today is deadline day...")

    gameweek = Gameweek.objects.get(gameweek_no=gameweek_no)
    gameweek_deadline_date = gameweek.deadline.date()

    # When this func returns true, todays_date will be midnight (UTC) next day
    # So go back one day
    todays_date = date.today()
    todays_date = todays_date - timedelta(days=1)

    if todays_date == gameweek_deadline_date:
        logger.info("Today is deadline day")
        return True

    else:
        logger.info("Today is not deadline day")
        return False


def is_final_gameweek_day(gameweek_no: int):
    """Checks if today is final day of the gameweek"""
    # Get all gamedays in gameweek
    gameweek_gamedays = list(
        Gameday.objects.filter(
            gameweek__gameweek_no=gameweek_no,
        )
    )

    # Sort by date
    gameweek_gamedays.sort(key=lambda x: x.date, reverse=True)
    final_gameday_date = gameweek_gamedays[0].date

    # Get todays date, make UTC aware
    utc = pytz.timezone("UTC")
    todays_date = utc.localize(datetime.today())

    if todays_date > final_gameday_date:
        return True
    else:
        return False


def check_choices(gameweek_no: int):
    logger.info("Checking for funballers who haven't submitted choices...")

    choices = list(
        Choices.objects.filter(
            gameweek__gameweek_no=gameweek_no,
        )
    )

    funballer_with_choice_ids = [choice.funballer_id for choice in choices]

    all_funballers = list(Funballer.objects.all())

    funballers_with_no_choices = [
        funballer
        for funballer in all_funballers
        if funballer.id not in funballer_with_choice_ids
    ]

    allocate_choices(
        funballers_with_no_choices=funballers_with_no_choices,
        gameweek_no=gameweek_no,
    )


def check_choices_if_deadline_day(gameweek_no: int):
    """If we're in deadline day, check all funballers have submitted a choice"""
    deadline_day = is_deadline_day(gameweek_no=gameweek_no)

    if deadline_day:
        check_choices(gameweek_no=gameweek_no)


def allocate_choices(
    funballers_with_no_choices: List[Funballer],
    gameweek_no: int,
):
    """Allocate a random team/player to each funballer who has not picked"""
    for funballer in funballers_with_no_choices:
        logger.info("Allocating random choices...")

        # Get list of teams already chosen by funballer
        all_funballer_choices = list(Choices.objects.filter(funballer=funballer))

        # Get all funballer's team picks
        funballer_team_choices = [
            choice.team_choice for choice in all_funballer_choices
        ]

        # Get all funballer's player picks
        funballer_player_choices = [
            choice.player_choice for choice in all_funballer_choices
        ]

        random_team = get_random_team(non_permitted_teams=funballer_team_choices)
        random_player = get_random_player(
            non_permitted_players=funballer_player_choices
        )

        # Get gameweek obj from gameweek no
        gameweek = Gameweek.objects.get(gameweek_no=gameweek_no)

        choice = Choices(
            funballer_id=funballer.id,
            gameweek=gameweek,
            team_choice=random_team,
            player_choice=random_player,
            team_has_been_steved=True,
            player_has_been_steved=True,
        )
        choice.save()
        logger.info(
            f"Funballer {funballer.first_name}, with id {funballer.id}, has been "
            f"allocated team: {random_team.team_name} and player: "
            f"{random_player.first_name} {random_player.surname}"
        )


def determine_players_fixture_has_finished(
    weekly_fixtures: List[Fixture],
    player: Player,
) -> bool:
    """Determines if a player's fixture has finished"""
    try:
        players_fixture = next(
            fixture
            for fixture in weekly_fixtures
            if player.team in {fixture.home_team, fixture.away_team}
        )
    except StopIteration:
        logger.info(
            f"{player.surname}'s team did not play this gameweek. Allocating new "
            f"player."
        )

        # By setting this to false, recursion continues and a new player is selected
        players_fixture_has_finished = False

        return players_fixture_has_finished

    players_fixture_kickoff = datetime.strptime(
        players_fixture.kickoff, "%Y-%m-%d %H:%M:%S"
    )

    # Make utc aware
    utc = pytz.timezone("UTC")
    players_fixture_kickoff_aware = utc.localize(players_fixture_kickoff)
    predicted_end_of_match = players_fixture_kickoff_aware + timedelta(hours=2)

    # Compare with todays date, in UTC - TODO: check UTC is correct
    current_datetime = datetime.now(tz=utc)

    if current_datetime > predicted_end_of_match:
        players_fixture_has_finished = True
    else:
        players_fixture_has_finished = False

    return players_fixture_has_finished


def determine_player_played_in_fixture(
    player: Player,
    fpl_players: List,
    raw_gameweek_player_data: List,
) -> bool:
    """Determine if player played in his team's fixture"""
    # Get players FPL API ID
    player_fpl_api_data = next(
        fpl_api_player
        for fpl_api_player in fpl_players
        if fpl_api_player["surname"] == player.surname
        and fpl_api_player["team"] == player.team.team_name
    )

    player_fpl_api_id = player_fpl_api_data["id"]

    # Check if player played in that fixture
    try:
        players_fpl_gameweek_stats = next(
            player
            for player in raw_gameweek_player_data
            if player["id"] == player_fpl_api_id
        )
    except StopIteration:
        # Seems not all players from FPL API appear in gameweek stats?
        player_played = False

    # Check minutes
    if players_fpl_gameweek_stats["stats"]["minutes"] == 0:
        player_played = False
    else:
        player_played = True

    return player_played


def assign_new_player_if_pick_did_not_play(
    player: Player,
    weekly_fixtures: List[Fixture],
    fpl_players: List,
    pick: Choices,
    raw_gameweek_player_data: List,
    player_played: bool = False,
) -> Player:
    """
    Takes a funballers player pick, if they did not play,
    a player is randomly selected to find a player which did play.
    """
    while not player_played:
        # Has that player's team played in this gameweek?
        players_fixture_has_finished = determine_players_fixture_has_finished(
            weekly_fixtures=weekly_fixtures,
            player=player,
        )

        if players_fixture_has_finished:
            player_played = determine_player_played_in_fixture(
                player=player,
                fpl_players=fpl_players,
                raw_gameweek_player_data=raw_gameweek_player_data,
            )

            if player_played:
                # Player has played -> Valid choice
                return player

            if not player_played:
                # Player didn't play -> allocate random player
                logger.info(
                    f"{player.surname} did not play. Allocating random choice for "
                    f"funballer with id {pick.funballer_id}"
                )

                # Get list of funballer's player picks so far
                funballer_player_picks = list(
                    Choices.objects.filter(
                        funballer_id=pick.funballer_id,
                    ).values("player_choice")
                )

                new_player = get_random_player(
                    non_permitted_players=funballer_player_picks,
                )
                return assign_new_player_if_pick_did_not_play(
                    player=new_player,
                    weekly_fixtures=weekly_fixtures,
                    fpl_players=fpl_players,
                    pick=pick,
                    raw_gameweek_player_data=raw_gameweek_player_data,
                    player_played=player_played,
                )

    return player


def check_player_picks_played(gameweek_no: int):
    """
    Checks that each funballer's player pick actually got on the pitch.
    If not, a random player is allocated to them
    """
    request_response = requests.get(
        url=f"https://fantasy.premierleague.com/api/event/{gameweek_no}/live/"
    )
    raw_gameweek_player_data = json.loads(request_response.content).get("elements")

    fpl_interface = FPLInterface()
    fpl_players = fpl_interface.retrieve_players()

    # Get players picked for this gameweek
    weekly_picks = list(Choices.objects.filter(gameweek__gameweek_no=gameweek_no))

    weekly_fixtures = list(
        Fixture.objects.filter(
            gameday__gameweek__gameweek_no=gameweek_no,
        )
    )

    for pick in weekly_picks:
        # Get player object using player_choice_id in choices
        player = Player.objects.get(id=pick.player_choice_id)

        new_player = assign_new_player_if_pick_did_not_play(
            player=player,
            weekly_fixtures=weekly_fixtures,
            fpl_players=fpl_players,
            pick=pick,
            raw_gameweek_player_data=raw_gameweek_player_data,
        )

        if new_player != player:
            logger.info(
                f"Funballer with id {pick.funballer_id} has been allocated"
                f" {new_player.surname}"
            )
            pick.player_choice = new_player
            pick.player_has_been_steved = True

        pick.save()


def check_lineups(gameweek_no: int):
    """Runs once the gameweek has finished, checks each funballer's player
    pick has played, if not, allocates a random player."""
    final_gameweek_day = is_final_gameweek_day(gameweek_no=gameweek_no)

    if final_gameweek_day:
        check_player_picks_played(gameweek_no=gameweek_no)


if __name__ == "__main__":
    prev_gameweek_no = determine_gameweek_no()
    check_choices(gameweek_no=prev_gameweek_no)
    check_player_picks_played(gameweek_no=prev_gameweek_no)
