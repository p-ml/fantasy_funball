import django

django.setup()

from fantasy_funball.models import Choices, Funballer, Gameweek, Player, Team


def insert_void_choices(gameweek_no: int) -> None:
    gameweek_choices = list(Choices.objects.all().filter(gameweek_id=gameweek_no))

    funballers_with_choices = [choice.funballer_id for choice in gameweek_choices]

    funballers_with_no_choices = [
        x for x in range(1, 11) if x not in funballers_with_choices
    ]

    # Get void player and team
    void_player = Player.objects.get(surname="Void")
    void_team = Team.objects.get(team_name="Gameweek Void")

    chosen_gameweek = Gameweek.objects.get(gameweek_no=gameweek_no)

    for funballer_id in funballers_with_no_choices:
        funballer = Funballer.objects.get(id=funballer_id)
        void_choice = Choices(
            funballer=funballer,
            gameweek=chosen_gameweek,
            team_choice=void_team,
            player_choice=void_player,
        )
        void_choice.save()
