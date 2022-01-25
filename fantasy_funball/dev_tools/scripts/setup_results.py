from datetime import datetime, timezone

from fantasy_funball.dev_tools.scripts.db_connection import database_connection
from fantasy_funball.models import Gameday, Player, Result, Team


def setup_results() -> None:
    # Wipe postgres result table before adding setting up
    conn = database_connection()
    conn.commit()
    conn.close()

    # Using team/player names for this script as ids are subject to change
    results = [
        {
            "home_team": "Spurs",
            "home_score": 10,
            "away_team": "Arsenal",
            "away_score": 0,
            "date": datetime.strptime(
                "2021-08-13 00:00:00.000000", "%Y-%m-%d %H:%M:%S.%f"
            ).replace(tzinfo=timezone.utc),
            "scorers": ["Harry Kane", "Hugo Lloris"],
            "assists": ["Tanguy Ndombele"],
        },
        {
            "home_team": "Chelsea",
            "home_score": 2,
            "away_team": "Brentford",
            "away_score": 8,
            "date": datetime.strptime(
                "2021-08-13 00:00:00.000000", "%Y-%m-%d %H:%M:%S.%f"
            ).replace(tzinfo=timezone.utc),
            "scorers": ["Timo Werner", "Ivan Toney"],
            "assists": ["Ivan Toney"],
        },
    ]

    for result in results:
        scorers_surnames = {x.split(" ")[1] for x in result["scorers"]}
        assists_surnames = {x.split(" ")[1] for x in result["assists"]}

        scorers = list(Player.objects.filter(surname__in=scorers_surnames))  # noqa: F841
        assists = list(Player.objects.filter(surname__in=assists_surnames))  # noqa: F841

        result_inst = Result(
            home_team=Team.objects.get(team_name=result["home_team"]),
            home_score=result["home_score"],
            away_team=Team.objects.get(team_name=result["away_team"]),
            away_score=result["away_score"],
            gameday=Gameday.objects.get(date=result["date"]),
        )
        result_inst.save()

        # TODO: Fix later (not high priority as only for local dev)
        # Model obj must be saved before adding many-to-many fields
        # result_inst.scorers.add(*scorers)
        # result_inst.assists.add(*assists)


if __name__ == "__main__":
    setup_results()
