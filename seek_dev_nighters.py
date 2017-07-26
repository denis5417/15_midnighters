import json
import requests
from datetime import datetime, time
import pytz

LINK = "https://devman.org/api/challenges/solution_attempts"


def load_attempts():
    attempts_data = json.loads(requests.get(LINK).text)
    pages_count = attempts_data['number_of_pages']
    for page in range(1, pages_count + 1):
        params = {"page": page}
        attempts_data = json.loads(requests.get(LINK, params=params).text)
        for attempt in attempts_data['records']:
            if attempt['timestamp']:  # sometimes data is invalid
                yield attempt


def get_midnighters():
    right_tz = pytz.timezone('Europe/Moscow')
    midnighters = []
    for attempt in load_attempts():
        attempt_date = pytz.timezone(attempt['timezone']).localize(datetime.fromtimestamp(attempt['timestamp']))
        right_attempt_time = attempt_date.astimezone(right_tz).time()
        if 0 <= right_attempt_time.hour() <= 5:
            midnighters.append(attempt['username'])
    return set(midnighters)  # usernames should not be repeated

if __name__ == '__main__':
    print(*get_midnighters(), sep="\n")