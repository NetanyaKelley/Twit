from flask import Flask, request
from collections import defaultdict, deque
from threading import Lock
from pathlib import Path
import json
import os
import random
import re
import time

app = Flask(__name__)

with Path(__file__).with_name('foods.json').open(encoding='utf-8') as file:
    foods = json.load(file)

MAX_WINS = 4
WINDOW_SECONDS = 60 * 60
PRIZE_POINTS = 3000
WIN_PROBABILITY = float(os.environ.get('CHEF_WIN_PROBABILITY', '0.20'))
if not 0 <= WIN_PROBABILITY <= 1:
    raise ValueError('CHEF_WIN_PROBABILITY must be between 0 and 1')

win_history = defaultdict(deque)
win_lock = Lock()

@app.get('/chef')
def chef():
    username = request.args.get('user', '').strip().lstrip('@').lower()
    if not re.fullmatch(r'[a-z0-9_]{1,25}', username):
        return 'Missing or invalid viewer username.', 400

    with win_lock:
        now = time.monotonic()
        history = win_history[username]
        while history and now - history[0] >= WINDOW_SECONDS:
            history.popleft()

        if len(history) >= MAX_WINS:
            food = random.choice(foods['bad_foods'])
            return f'🤢 The chef served {food}! DISGUSTING! (Hourly win limit reached.)'

        if random.random() >= WIN_PROBABILITY:
            food = random.choice(foods['bad_foods'])
            return f'🤢 The chef served {food}! DISGUSTING!'

        history.append(now)
        food = random.choice(foods['good_foods'])
        return (
            f'🍽️ The chef served {food}! DELICIOUS! '
            f'🎉 @{username} wins a 3000-point prize (manual payout required)! '
        )
