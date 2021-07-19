from typing import List

import django

django.setup()

from fantasy_funball.models import Choices, Funballer, Result


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
            winner = None

        winning_teams.append(winner)

    return winning_teams


def get_gameweek_results(gameweek_no: int) -> List:
    gameweek_results_queryset = Result.objects.filter(
        gameday__gameweek__gameweek_no=gameweek_no
    )

    # Convert queryset to list of results
    gameweek_results = list(gameweek_results_queryset)

    winning_teams = determine_gameweek_winners(gameweek_results=gameweek_results)

    return winning_teams


def get_weekly_team_picks(gameweek_no: int) -> List:
    # Scan choices to check for chosen teams
    weekly_team_picks = Choices.objects.filter(gameweek_id__gameweek_no=gameweek_no)

    # Convert QuerySet to list
    weekly_team_picks = list(weekly_team_picks)

    return weekly_team_picks


def update_standings(gameweek_no: int):
    gameweek_winners = get_gameweek_results(gameweek_no=gameweek_no)
    weekly_team_picks = get_weekly_team_picks(gameweek_no=gameweek_no)

    # Extract winning team ids
    gameweek_winner_ids = {team.id for team in gameweek_winners}

    for pick in weekly_team_picks:
        if pick.team_choice_id in gameweek_winner_ids and not pick.has_been_processed:
            # Increment funballer team_points
            funballer = Funballer.objects.get(
                id=pick.funballer_id,
            )
            funballer.team_points += 1
            funballer.points = funballer.team_points + funballer.player_points
            funballer.save()

            # Mark choice as processed
            pick.has_been_processed = True
            pick.save()


if __name__ == "__main__":
    results = get_gameweek_results(gameweek_no=1)
    update_standings(gameweek_no=1)
