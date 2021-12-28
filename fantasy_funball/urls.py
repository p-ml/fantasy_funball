from django.urls import path

from fantasy_funball.views.choices import (
    FunballerGetChoiceView,
    FunballerPostChoiceView,
    FunballerRemainingTeamChoice,
)
from fantasy_funball.views.fixtures import (
    RetrieveAllGameweeks,
    RetrieveFixture,
    RetrieveGameday,
    RetrieveGameweek,
    UpdateGameweekFixtures,
)
from fantasy_funball.views.funballer import FunballerView, SingleFunballerView
from fantasy_funball.views.gameweek_summary import GameweekSummaryViewset
from fantasy_funball.views.player import PlayerTeamView, PlayerView
from fantasy_funball.views.update_database import UpdateDatabaseView

urlpatterns = [
    path("funballer/<int:id>", SingleFunballerView.as_view(), name="funballer-detail"),
    path("funballer/", FunballerView.as_view(), name="funballer"),
    path(
        "funballer/choices/submit/<str:pin>",
        FunballerPostChoiceView.as_view(),
        name="funballer-post-choices",
    ),
    path(
        "funballer/choices/<str:funballer_name>",
        FunballerGetChoiceView.as_view(),
        name="funballer-get-choices",
    ),
    path("fixture/<int:id>", RetrieveFixture.as_view(), name="retrieve-fixture"),
    path("gameday/<int:id>", RetrieveGameday.as_view(), name="retrieve-gameday"),
    path(
        "gameweek/<int:gameweek_no>",
        RetrieveGameweek.as_view(),
        name="retrieve-gameweek",
    ),
    path(
        "gameweek/all/",
        RetrieveAllGameweeks.as_view(),
        name="retrieve-all-gameweeks",
    ),
    path(
        "gameweek/<int:gameweek_no>/update_fixtures/",
        UpdateGameweekFixtures.as_view(),
        name="update-fixtures",
    ),
    path(
        "gameweek/summary/", GameweekSummaryViewset.as_view(), name="gameweek-summary"
    ),
    path("<str:team_name>/players/", PlayerTeamView.as_view(), name="retrieve-players"),
    path("players/", PlayerView.as_view(), name="retrieve-all-players"),
    path("update_database/", UpdateDatabaseView.as_view(), name="update-database"),
    path(
        "funballer/choices/valid_teams/<str:funballer_name>",
        FunballerRemainingTeamChoice.as_view(),
        name="funballer-valid-teams-picks",
    ),
]
