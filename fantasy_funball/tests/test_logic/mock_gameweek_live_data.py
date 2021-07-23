from typing import Dict


def mock_gameweek_live_data() -> Dict:
    """Mock FPL API gameweek live response. To be used for getting weekly
    scorers and assists"""
    return {
        "elements": [
            {
                "id": 390,  # Player's id
                "stats": {
                    "minutes": 72,
                    "goals_scored": 2,
                    "assists": 1,
                    "clean_sheets": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0,
                    "penalties_missed": 0,
                    "yellow_cards": 0,
                    "red_cards": 0,
                    "saves": 0,
                    "bonus": 3,
                    "bps": 64,
                    "influence": "91.4",
                    "creativity": "62.2",
                    "threat": "52.0",
                    "ict_index": "20.6",
                    "total_points": 18,
                    "in_dreamteam": True,
                },
                "explain": [
                    {
                        "fixture": "35",
                        "stats": [
                            {
                                "identifier": "minutes",
                                "points": 2,
                                "value": 72,
                            },
                            {
                                "identifier": "goals_scored",
                                "points": 10,
                                "value": 2,
                            },
                            {
                                "identifier": "assists",
                                "points": 3,
                                "value": 1,
                            },
                            {
                                "identifier": "bonus",
                                "points": 3,
                                "value": 3,
                            },
                        ],
                    }
                ],
            }
        ],
    }
