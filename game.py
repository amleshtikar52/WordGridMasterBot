from collections import defaultdict

active_games = {}

def start_game(chat_id, grid_size):
    active_games[chat_id] = {
        "grid": grid_size,
        "round": 1,
        "words": [],
        "found": set(),
        "players": defaultdict(int),
        "active": True
    }

def end_game(chat_id):
    if chat_id in active_games:
        del active_games[chat_id]

def get_game(chat_id):
    return active_games.get(chat_id)
