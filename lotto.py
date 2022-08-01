import os
import random
from collections import Counter
from heapq import nlargest

import pandas as pd
import requests
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

# supabase client connection
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def generate_numbers(ticket: str) -> list[int]:
    """If you're feeling lucky you can generarte your own numbers"""
    numbers = []

    if ticket == "euros":
        numbers.extend(random.sample(range(1, 50 + 1), 5))
        numbers.extend(random.sample(range(1, 13 + 1), 2))

    elif ticket == "lotto":
        numbers.extend(random.sample(range(1, 60 + 1), 6))

    return numbers


def download_latest_lotto_draw_file() -> bool:
    """
    Downloads the latest draw history from the website.
    Then adds them into a supabase database if no date is duplicated.

    https://www.national-lottery.co.uk/results/euromillions/draw-history/csv

    """
    res = requests.get(
        "https://www.national-lottery.co.uk/results/lotto/draw-history/csv"
    )
    with open("./data/draw-history.csv", "wb") as f:
        f.write(res.content)

    df = pd.read_csv("./data/draw-history.csv")
    stripped_numbers = df[
        [
            "DrawDate",
            "Ball 1",
            "Ball 2",
            "Ball 3",
            "Ball 4",
            "Ball 5",
            "Ball 6",
            "Bonus Ball",
        ]
    ]

    number_row: list = []
    number_row.extend(stripped_numbers.values.tolist())

    # added each "draw_date" into a list to check for duplicates
    # when putting new data into the database
    draw_dates: list = [
        date["draw_date"]
        for date in supabase.table("lotto_draw_history")
        .select("draw_date")
        .execute()
        .data
    ]

    for num in number_row:

        if num[0] not in draw_dates:

            row = {
                "draw_date": num[0],
                "ball_1": num[1],
                "ball_2": num[2],
                "ball_3": num[3],
                "ball_4": num[4],
                "ball_5": num[5],
                "ball_6": num[6],
                "bonus_ball": num[7],
            }

            # insert row into supabase when no duplicate dates are found.
            supabase.table("lotto_draw_history").insert(row).execute()

    return True


def drawn_lotto_numbers() -> dict:
    """
    Collects draw history from supabase. Then returns a dictionary
    with a list of drawn numbers and drawn lucky_stars
    """

    drawn_numbers: list[int] = []

    # get the latest draw numbers from the database
    json_data = supabase.table("lotto_draw_history").select("*").execute()

    # put drawn numbers in a list to check common numbers
    for number in json_data.data:
        drawn_numbers.extend(
            (
                number["ball_1"],
                number["ball_2"],
                number["ball_3"],
                number["ball_4"],
                number["ball_5"],
                number["ball_6"],
                number["bonus_ball"],
            )
        )

    return dict(drawn_numbers=drawn_numbers)


def collect_duplicate_lotto_numbers() -> dict:
    """Collect the drawn numbers and count them to return them sorted"""

    data = drawn_lotto_numbers()

    numbers = Counter(data["drawn_numbers"]).most_common()

    return dict(lotto=numbers)


def common_lotto_generator() -> list:

    """
    This takes the top 6 numbers from get_highest_lotto_count and generates a list
    from the all the numbers that have the same 2nd index.

    Then generates a random 6 digit number from the list.
    """
    data = collect_duplicate_lotto_numbers()
    numbers = data["lotto"]
    counts = set(nlargest(6, {count for _, count in numbers}))

    common_numbers: list = [number for number, count in numbers if count in counts]
    return random.sample(common_numbers, 6)
