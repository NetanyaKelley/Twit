import json
import random
from pathlib import Path

FOODS = json.loads((Path(__file__).parent / "foods.json").read_text(encoding="utf-8"))

def chef(username="viewer"):
    good = random.random() < 0.20
    category = "good_foods" if good else "bad_foods"
    food = random.choice(FOODS[category])
    emoji = "🍽️" if good else "🤢"
    return f"{emoji} {username} opens the fridge and gets: {food}!"

if __name__ == "__main__":
    for _ in range(10):
        print(chef())
