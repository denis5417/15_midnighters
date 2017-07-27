import json
import requests
from datetime import datetime
import pytz


def load_attempts(link):
    attempts_data = json.loads(requests.get(link).text)
    pages_count = attempts_data['number_of_pages']
    if attempts_data['records'][0]['timestamp']:
        yield attempts_data['records'][0]['timestamp']
    for page in range(2, pages_count+1):
        params = {"page": page}
        attempts_data = json.loads(requests.get(link, params=params).text)
        for attempt in attempts_data['records']:
            if attempt['timestamp']:  # sometimes data is invalid
                yield attempt


def get_midnighters():
    right_tz = pytz.timezone('Europe/Moscow')
    midnighters = []
    for attempt in load_attempts("https://devman.org/api/challenges/solution_attempts"):
        attempt_date = pytz.timezone(attempt['timezone']).localize(datetime.fromtimestamp(attempt['timestamp']))
        right_attempt_time = attempt_date.astimezone(right_tz).time()
        start_of_night = 0
        end_of_night = 5
        if start_of_night <= right_attempt_time.hour <= end_of_night:
            midnighters.append(attempt['username'])
    return set(midnighters)  # usernames should not be repeated

if __name__ == '__main__':
    print(*get_midnighters(), sep="\n")