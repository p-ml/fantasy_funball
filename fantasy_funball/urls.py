from django.urls import path

from fantasy_funball.views.fixtures import (
    RetrieveFixture,
    RetrieveGameday,
    RetrieveGameweek,
)
from fantasy_funball.views.funballer import CreateFunballerView, ModifyFunballerView

urlpatterns = [
    path("funballer/<int:id>", ModifyFunballerView.as_view(), name="funballer-detail"),
    path("funballer/", CreateFunballerView.as_view(), name="create-funballer"),
    path("fixture/<int:id>", RetrieveFixture.as_view(), name="retrieve-fixture"),
    path("gameday/<int:id>", RetrieveGameday.as_view(), name="retrieve-gameday"),
    path("gameweek/<int:id>", RetrieveGameweek.as_view(), name="retrieve-gameweek"),
]
