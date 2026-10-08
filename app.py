from flask import Flask
import random
import json
from pathlib import Path

app = Flask(__name__)

MODERATORS = [
    "@sardyyyy",
]

foods_path = Path(__file__).with_name("foods.json")
with open(foods_path, encoding="utf-8") as f:
    foods = json.load(f)

@app.route("/chef")
def chef():
    if random.random() < 0.80:
        food = random.choice(foods["bad_foods"])
        return f"🤢 The chef served {food}! DISGUSTING!"

    food = random.choice(foods["good_foods"])

    return (
        f"🍽️ The chef served {food}! DELICIOUS! "
        f"🎉 @sardyyyy, please award the winner 3000 points!"
    )