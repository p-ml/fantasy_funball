from django.urls import path

from fantasy_funball.views.fixtures import (
    RetrieveFixture,
    RetrieveGameday,
    RetrieveGameweek,
)
from fantasy_funball.views.funballer import (
    FunballerChoiceView,
    FunballerView,
    SingleFunballerView,
)

urlpatterns = [
    path("funballer/<int:id>", SingleFunballerView.as_view(), name="funballer-detail"),
    path("funballer/", FunballerView.as_view(), name="funballer"),
    path(
        "funballer/choices/<str:funballer_name>",
        FunballerChoiceView.as_view(),
        name="funballer-choices",
    ),
    path("fixture/<int:id>", RetrieveFixture.as_view(), name="retrieve-fixture"),
    path("gameday/<int:id>", RetrieveGameday.as_view(), name="retrieve-gameday"),
    path(
        "gameweek/<int:gameweek_no>",
        RetrieveGameweek.as_view(),
        name="retrieve-gameweek",
    ),
]
