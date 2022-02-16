import csv
from datetime import datetime

import tweepy

NUMBER_TO_WORD_MAP = dict()
with open("etc/wordle_answers.csv") as f:
    reader = csv.reader(f, delimiter="\t")
    # skip the header
    next(reader)
    for row in reader:
        date, puzzle_number, word = row
        NUMBER_TO_WORD_MAP[int(puzzle_number)] = word


class WordleStatsTweet:
    def __init__(self, tweet: tweepy.Tweet):
        # split the tweet into lines, discard the empty lines since not all
        # tweets have the empty line between hardmode count and first score
        tweet_lines = [l for l in tweet.text.splitlines() if l]
        _, puzzle_number, date_str = tweet_lines[0].split()
        self.puzzle_number = int(puzzle_number)
        self.word = NUMBER_TO_WORD_MAP[self.puzzle_number]
        self.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        self.results = int(tweet_lines[1].split()[0].replace(",", ""))
        self.pct_1 = int(tweet_lines[3].split()[-1].strip("%")) / 100.0
        self.pct_2 = int(tweet_lines[4].split()[-1].strip("%")) / 100.0
        self.pct_3 = int(tweet_lines[5].split()[-1].strip("%")) / 100.0
        self.pct_4 = int(tweet_lines[6].split()[-1].strip("%")) / 100.0
        self.pct_5 = int(tweet_lines[7].split()[-1].strip("%")) / 100.0
        self.pct_6 = int(tweet_lines[8].split()[-1].strip("%")) / 100.0
        self.pct_fail = int(tweet_lines[9].split()[-1].strip("%")) / 100.0
        self.scores_array = [
            self.pct_1,
            self.pct_2,
            self.pct_3,
            self.pct_4,
            self.pct_5,
            self.pct_6,
            self.pct_fail,
        ]
        # need the 1 offset cause 0 index
        self.modal_score = self.scores_array.index(max(self.scores_array)) + 1
        if self.modal_score > 6:
            self.modal_score = "X"

    @property
    def values(self) -> tuple:
        return (
            self.date,
            self.puzzle_number,
            self.word,
            self.results,
            self.pct_1,
            self.pct_2,
            self.pct_3,
            self.pct_4,
            self.pct_5,
            self.pct_6,
            self.pct_fail,
            self.modal_score,
        )
