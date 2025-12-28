import random
from datetime import datetime

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def create_game(size):
    grid = [[random.choice(ALPHABET) for _ in range(size)] for _ in range(size)]
    return {
        "grid": grid,
        "size": size,
        "start": datetime.utcnow(),
        "found": set(),
        "round": 1
    }
