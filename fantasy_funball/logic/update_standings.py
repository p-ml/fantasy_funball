import logging
from collections import namedtuple
from typing import List, Set

import django

django.setup()

from fantasy_funball.models import Choices, Funballer, Result
from fantasy_funball.models.players import Assists, Goals

ScorerAssistIds = namedtuple("ScorerAssistIds", ["scorer_ids", "assist_ids"])

logger = logging.getLogger("papertrail")


def determine_gameweek_winners(gameweek_results: List[Result]) -> List:
    # Establish list of winning teams
    winning_teams = []
    for match in gameweek_results:
        if match.home_score > match.away_score:
            # Home team is winner
            winner = match.home_team

        elif match.home_score < match.away_score:
            # Away team is winner
            winner = match.away_team

        else:
            # Draw
            continue

        winning_teams.append(winner)

    return winning_teams


def get_gameweek_results(gameweek_no: int) -> List:
    gameweek_results = Result.objects.filter(gameday__gameweek__gameweek_no=gameweek_no)

    # Convert queryset to list of results
    gameweek_results = list(gameweek_results)

    winning_teams = determine_gameweek_winners(gameweek_results=gameweek_results)

    return winning_teams


def get_weekly_team_picks(gameweek_no: int) -> List:
    # Scan choices to check for chosen teams
    weekly_team_picks = Choices.objects.filter(gameweek_id__gameweek_no=gameweek_no)

    # Convert QuerySet to list
    weekly_team_picks = list(weekly_team_picks)

    return weekly_team_picks


def get_weekly_scorers(weekly_result_data: List) -> Set:
    """Get ids of players who scored in given gameweek"""
    scorer_ids = set()
    for result in weekly_result_data:
        result_scorer_data = list(Goals.objects.filter(result_id=result.id))
        result_scorer_ids = {goal.player_id for goal in result_scorer_data}

        scorer_ids.update(result_scorer_ids)

    return scorer_ids


def get_weekly_assists(weekly_result_data: List) -> Set:
    """Get ids of players who assisted in given gameweek"""
    assist_ids = set()
    for result in weekly_result_data:
        result_assist_data = list(Assists.objects.filter(result_id=result.id))
        result_assist_ids = {assist.player_id for assist in result_assist_data}

        assist_ids.update(result_assist_ids)

    return assist_ids


def get_weekly_scorers_and_assists(gameweek_no: int) -> ScorerAssistIds:
    weekly_result_data = Result.objects.filter(
        gameday__gameweek__gameweek_no=gameweek_no
    )

    # Convert QuerySet to list
    weekly_result_data = list(weekly_result_data)

    scorer_ids = get_weekly_scorers(weekly_result_data=weekly_result_data)
    assist_ids = get_weekly_assists(weekly_result_data=weekly_result_data)

    return ScorerAssistIds(
        scorer_ids=scorer_ids,
        assist_ids=assist_ids,
    )


def update_standings(gameweek_no: int):
    gameweek_winners = get_gameweek_results(gameweek_no=gameweek_no)
    weekly_team_picks = get_weekly_team_picks(gameweek_no=gameweek_no)

    # Extract winning team ids
    gameweek_winner_ids = {team.id for team in gameweek_winners}

    scorer_assist_ids = get_weekly_scorers_and_assists(gameweek_no=gameweek_no)
    scorer_ids = scorer_assist_ids.scorer_ids
    assist_ids = scorer_assist_ids.assist_ids

    for pick in weekly_team_picks:
        if not pick.team_has_been_processed:
            if pick.team_choice_id in gameweek_winner_ids:
                # Increment funballer team_points
                funballer = Funballer.objects.get(
                    id=pick.funballer_id,
                )
                funballer.team_points += 1
                funballer.points = funballer.team_points + funballer.player_points
                funballer.save()

                logger.info(
                    f"Funballer {funballer.first_name}, with id {funballer.id}, has "
                    f"been awarded 1 point as their team won."
                )

                # Mark team choice as processed
                pick.team_has_been_processed = True
                pick.save()

        if not pick.player_has_been_processed:
            if (
                pick.player_choice_id in scorer_ids
                or pick.player_choice_id in assist_ids
            ):
                # Increment funballer player_points
                funballer = Funballer.objects.get(
                    id=pick.funballer_id,
                )
                funballer.player_points += 1
                funballer.points = funballer.team_points + funballer.player_points
                funballer.save()

                logger.info(
                    f"Funballer {funballer.first_name}, with id {funballer.id}, has "
                    f"been awarded 1 point as their player scored or assisted."
                )

                # Mark player choice as processed
                pick.player_has_been_processed = True
                pick.save()


if __name__ == "__main__":
    get_weekly_scorers_and_assists(gameweek_no=4)
