from datetime import date, datetime, timedelta
from os import environ
import sqlite3
from typing import List

import tweepy
from loguru import logger

from db import initialize
from tweet import WordleStatsTweet


db_location = environ.get("WORDLE_STATS_STORAGE_LOC") or "data/wordle.db"
con = sqlite3.connect(db_location)
con.row_factory = sqlite3.Row
initialize(con)


def get_max_date(
    con: sqlite3.Connection, table: str, date_fallback: date, date_column: str = "date"
):
    max_date_sql = f"select max({date_column}) as max_date from {table}"
    with con:
        cursor = con.cursor()
        cursor.execute(max_date_sql)
        max_date = cursor.fetchone()["max_date"]

    if max_date:
        return datetime.strptime(max_date, "%Y-%m-%d")
    return date_fallback


def extract_tweets(start_datetime: datetime) -> List[tweepy.Tweet]:
    client = tweepy.Client(environ["TWITTER_API_BEARER_TOKEN"])
    user = client.get_user(username="WordleStats")
    tweets = client.get_users_tweets(
        id=user.data.id,
        start_time=start_datetime.isoformat() + "Z",
        max_results=100,
        exclude="retweets,replies",
    ).data
    return tweets


def main():
    watermark = get_max_date(con, "solution_stats", date(2022, 1, 6))
    day_after_watermark = watermark + timedelta(days=1)
    logger.info(f"Extracting tweets after {watermark}")
    tweets = extract_tweets(datetime.combine(day_after_watermark, datetime.min.time()))
    if tweets:
        logger.info(f"Inserting {len(tweets)} days of wordle solution stats")
        values = [
            WordleStatsTweet(tweet).values
            for tweet in tweets
            if tweet.text.startswith("#Wordle")
        ]
        with con:
            con.executemany(
                "INSERT into solution_stats(date, puzzle_number, word, results, pct_1, pct_2, pct_3, pct_4, pct_5, pct_6, pct_fail, modal_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                values,
            )


if __name__ == "__main__":
    main()
