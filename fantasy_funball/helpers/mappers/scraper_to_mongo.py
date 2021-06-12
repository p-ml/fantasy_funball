from datetime import datetime
from typing import Dict

import pytz


def scraper_deadline_to_datetime_mongo(date: Dict) -> datetime:
    """
    Converts date from FPL website in format:
        "Mon 1 Oct 10:00" (str)
    to:
        "2021-10-01 10:00:00" (datetime object)
    for database storage
    """
    date_data = list(date.values())[0]

    # Append year to date from scraper
    # TODO: Add support for next calendar year (2022)
    date_data = f"2021 {date_data}"

    # To datetime obj
    datetime_obj_unaware = datetime.strptime(date_data, "%Y %a %d %b %H:%M")

    # Make datetime tz aware
    bst = pytz.timezone("Europe/London")
    datetime_obj = bst.localize(datetime_obj_unaware)

    return datetime_obj


def scraper_date_to_datetime_mongo(date: str) -> datetime:
    """
    Converts date from FPL website in format:
        "Monday 1 October 2021" (str)
    to:
        "2021-10-01 00:00:00" (datetime object)
    for database storage
    """
    # To datetime obj
    datetime_obj_unaware = datetime.strptime(date, "%A %d %B %Y")

    # Make datetime tz aware
    bst = pytz.timezone("Europe/London")
    datetime_obj = bst.localize(datetime_obj_unaware)

    return datetime_obj


def scraper_fixture_to_mongo(data: Dict) -> Dict:
    fixture_data = list(data.values())[0]

    # fixture_data will be in format:
    # home_team home_score:away_score away_team
    fixture_split = fixture_data.split(":")

    output_format = {
        "home_team": fixture_split[0][0:-2],
        "home_score": fixture_split[0][-1],
        "away_team": fixture_split[1][2:],
        "away_score": fixture_split[1][0],
    }

    return output_format
