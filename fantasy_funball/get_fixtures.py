from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://fantasy.premierleague.com/fixtures"
N_GAMEWEEKS = 38


def parse_fixtures(gameweek_raw_text: List[str]) -> List[Dict]:
    game_data = []
    for matchday in gameweek_raw_text:
        split_text = matchday.split("\n")

        int_data = {"date": split_text[0], "matches": []}

        # Get no of games, first obj will be the date
        no_fixtures = int((len(split_text) - 1) / 4)
        for i in range(no_fixtures):
            start = i * 4
            int_game_data = {
                f"game_{i}": f"{split_text[start+1]} {split_text[start+2]}:"
                             f"{split_text[start+3]} {split_text[start+4]}"
            }
            int_data["matches"].append(int_game_data)

        game_data.append(int_data)

    return game_data


def get_weekly_fixtures(week: int) -> List[Dict]:
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    DRIVER_PATH = "/Users/patrick/Downloads/chromedriver"
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(f"{BASE_URL}/{week}/")
    gameweek_fixtures_raw = driver.find_elements_by_xpath(
        xpath="//div[@class='sc-bdnxRM icEFRW']"
    )

    gameweek_raw_text = [x.text for x in gameweek_fixtures_raw]

    gameweek_data = parse_fixtures(gameweek_raw_text=gameweek_raw_text)

    return gameweek_data


def get_gameweek_start_time(week: int) -> Dict:
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    DRIVER_PATH = "/Users/patrick/Downloads/chromedriver"
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(f"{BASE_URL}/{week}/")

    print(f"GAMEWEEK: {week}")

    gameweek_start_time_raw = driver.find_elements_by_xpath(
        xpath="//h2[@class='Fixtures__Deadline-sc-199hb1h-0 cFvJAa']"
    )[0].text

    # Strip "Gameweek N"
    gameweek_start_time = gameweek_start_time_raw.split("-")[1][1:]

    return {f"gameweek_{week}_start_time": gameweek_start_time}


def get_yearly_fixtures() -> List[Dict]:
    yearly_data = []
    for i in range(1, N_GAMEWEEKS + 1):

        gameweek_start_time = get_gameweek_start_time(week=i)

        week_data = get_weekly_fixtures(week=i)
        yearly_int_data = {
            f"gameweek_{i}_fixtures": week_data,
            f"gameweek_{i}_deadline": gameweek_start_time,
        }
        yearly_data.append(yearly_int_data)

    return yearly_data


if __name__ == "__main__":
    get_yearly_fixtures()
