import random
import string
from database import cur, conn

ACTIVE_GAMES = {}

def generate_grid(size):
    return [[random.choice(string.ascii_uppercase) for _ in range(size)] for _ in range(size)]

def generate_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def unique_word(length):
    while True:
        w = generate_word(length)
        cur.execute("SELECT word FROM global_words WHERE word=?", (w,))
        if not cur.fetchone():
            cur.execute("INSERT INTO global_words VALUES (?)", (w,))
            conn.commit()
            return w

def start_game(chat_id, size):
    round_words = []
    for i in range(3, size + 1):
        round_words.append(unique_word(i))

    ACTIVE_GAMES[chat_id] = {
        "grid": generate_grid(size),
        "words": round_words,
        "found": set(),
        "size": size
    }

def check_word(chat_id, word):
    game = ACTIVE_GAMES.get(chat_id)
    if not game:
        return False
    if word in game["words"] and word not in game["found"]:
        game["found"].add(word)
        return True
    return False

def end_game(chat_id):
    if chat_id in ACTIVE_GAMES:
        del ACTIVE_GAMES[chat_id]
