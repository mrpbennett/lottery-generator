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


def download_latest_euro_draw_file() -> bool:
    """
    Downloads the latest draw history from the website.
    Then adds them into a supabase database if no date is duplicated.

    https://www.national-lottery.co.uk/results/euromillions/draw-history/csv

    """
    res = requests.get(
        "https://www.national-lottery.co.uk/results/euromillions/draw-history/csv"
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
            "Lucky Star 1",
            "Lucky Star 2",
        ]
    ]

    number_row: list = []
    number_row.extend(stripped_numbers.values.tolist())

    # added each "draw_date" into a list to check for duplicates
    # when putting new data into the database
    draw_dates: list = [
        date["draw_date"]
        for date in supabase.table("euro_draw_history")
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
                "lucky_star_1": num[6],
                "lucky_star_2": num[7],
            }

            # insert row into supabase when no duplicate dates are found.
            supabase.table("euro_draw_history").insert(row).execute()

    return True


def drawn_euro_numbers() -> dict:
    """
    Collects non duplicate draw history from supabase. Then returns a dictionary
    with a list of drawn numbers and drawn lucky_stars
    """

    drawn_numbers: list[int] = []
    drawn_stars: list[int] = []

    # get the latest draw numbers from the database
    json_data = supabase.table("euro_draw_history").select("*").execute()

    # put drawn numbers in a list to check common numbers
    for number in json_data.data:
        drawn_numbers.extend(
            (
                number["ball_1"],
                number["ball_2"],
                number["ball_3"],
                number["ball_4"],
                number["ball_5"],
            )
        )
        drawn_stars.extend((number["lucky_star_1"], number["lucky_star_2"]))

    return dict(numbers=drawn_numbers, stars=drawn_stars)


def collect_duplicate_euro_numbers() -> dict:
    """Collect the drawn numbers and stars and counts them to return them sorted"""

    data: dict = drawn_euro_numbers()

    numbers: list = Counter(data["numbers"]).most_common()
    stars: list = Counter(data["stars"]).most_common()

    return dict(numbers=numbers, stars=stars)


def common_euros_generator() -> dict:

    data = collect_duplicate_euro_numbers()

    numbers: list = data["numbers"]
    stars: list = data["stars"]

    number_counts: set = set(nlargest(5, {count for _, count in numbers}))
    star_counts: set = set(nlargest(2, {count for _, count in stars}))

    common_numbers: list = [
        number for number, count in numbers if count in number_counts
    ]
    common_stars: list = [star for star, count in stars if count in star_counts]

    return dict(
        numbers=random.sample(common_numbers, 5),
        stars=random.sample(common_stars, 2),
    )
