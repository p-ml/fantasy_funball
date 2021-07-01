from unittest import TestCase
from unittest.mock import patch

from fantasy_funball.scraping.fixture_scraper import FixtureScraper

FIXTURE_SCRAPER_MODULE_PATH = "fantasy_funball.scraping.fixture_scraper"


class MockWebElement:
    """Dummy class for mocking return values"""

    pass


class TestGetFixtures(TestCase):
    @patch(f"{FIXTURE_SCRAPER_MODULE_PATH}.webdriver")
    def setUp(self, mock_webdriver) -> None:
        mock_webdriver_inst = mock_webdriver.return_value
        mock_webdriver_inst.return_value = {}
        self.fixture_scraper = FixtureScraper()

    @patch(f"{FIXTURE_SCRAPER_MODULE_PATH}.webdriver.Chrome")
    def test_get_gameweek_start_time(self, mock_webdriver):
        mock_webdriver_inst = mock_webdriver.return_value
        mock_webdriver_inst.return_value = {}

        mock_web_element = MockWebElement()
        mock_web_element.text = "Gameweek 1 - Sat 12 Sep 11:00"

        mock_webdriver_inst.get.return_value = {}
        mock_webdriver_inst.find_elements_by_xpath.return_value = [mock_web_element]

        fixture_scraper = FixtureScraper()

        response = fixture_scraper.get_gameweek_start_time(
            week=1,
        )

        expected_output = {"gameweek_1_start_time": "Sat 12 Sep 11:00"}

        self.assertEqual(response, expected_output)

    # TODO
    def test_get_weekly_fixtures(self):
        pass

    # TODO
    def test_get_yearly_fixtures(self):
        pass

    def test_parse_results(self):
        mock_raw_gameweek_text = [
            "Saturday 12 September 2020\n"
            "Fulham\n0\n3\nArsenal\n"
            "Crystal Palace\n1\n0\nSouthampton\n"
            "Liverpool\n4\n3\nLeeds\n"
            "West Ham\n0\n2\nNewcastle",
            "Sunday 13 September 2020\n"
            "West Brom\n0\n3\nLeicester\n"
            "Spurs\n0\n1\nEverton",
            "Monday 14 September 2020\n"
            "Sheffield Utd\n0\n2\nWolves\n"
            "Brighton\n1\n3\nChelsea",
        ]

        expected_output = [
            {
                "date": "Saturday 12 September 2020",
                "matches": [
                    {"game_0": "Fulham 0:3 Arsenal"},
                    {"game_1": "Crystal Palace 1:0 Southampton"},
                    {"game_2": "Liverpool 4:3 Leeds"},
                    {"game_3": "West Ham 0:2 Newcastle"},
                ],
            },
            {
                "date": "Sunday 13 September 2020",
                "matches": [
                    {"game_0": "West Brom 0:3 Leicester"},
                    {"game_1": "Spurs 0:1 Everton"},
                ],
            },
            {
                "date": "Monday 14 September 2020",
                "matches": [
                    {"game_0": "Sheffield Utd 0:2 Wolves"},
                    {"game_1": "Brighton 1:3 Chelsea"},
                ],
            },
        ]

        response = self.fixture_scraper.parse_results(mock_raw_gameweek_text)
        self.assertEqual(response, expected_output)

    def test_parse_fixtures(self):
        mock_raw_gameweek_text = [
            "Friday 13 August 2021\n" "Brentford\n20:00\nArsenal\n",
            "Saturday 14 August 2021\n"
            "Man Utd\n12:30\nLeeds\n"
            "Burnley\n15:00\nBrighton\n"
            "Chelsea\n15:00\nCrystal Palace\n"
            "Everton\n15:00\nSouthampton\n"
            "Leicester\n15:00\nWolves\n"
            "Watford\n15:00\nAston Villa\n"
            "Norwich\n17:30\nLiverpool\n",
            "Sunday 15 August 2021\n"
            "Newcastle\n14:00\nWest Ham\n"
            "Spurs\n16:30\nMan City",
        ]

        expected_output = [
            {
                "date": "Friday 13 August 2021",
                "matches": [{"game_0": "Brentford v Arsenal", "kickoff": "20:00"}],
            },
            {
                "date": "Saturday 14 August 2021",
                "matches": [
                    {"game_0": "Man Utd v Leeds", "kickoff": "12:30"},
                    {"game_1": "Burnley v Brighton", "kickoff": "15:00"},
                    {"game_2": "Chelsea v Crystal Palace", "kickoff": "15:00"},
                    {"game_3": "Everton v Southampton", "kickoff": "15:00"},
                    {"game_4": "Leicester v Wolves", "kickoff": "15:00"},
                    {"game_5": "Watford v Aston Villa", "kickoff": "15:00"},
                    {"game_6": "Norwich v Liverpool", "kickoff": "17:30"},
                ],
            },
            {
                "date": "Sunday 15 August 2021",
                "matches": [
                    {"game_0": "Newcastle v West Ham", "kickoff": "14:00"},
                    {"game_1": "Spurs v Man City", "kickoff": "16:30"},
                ],
            },
        ]

        response = self.fixture_scraper.parse_fixtures(mock_raw_gameweek_text)
        self.assertEqual(response, expected_output)
