import sqlite3

conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    score INTEGER DEFAULT 0,
    words_found INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS global_words (
    word TEXT PRIMARY KEY
)
""")

conn.commit()

def get_user(user_id, username):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.execute(
            "INSERT INTO users (user_id, username) VALUES (?,?)",
            (user_id, username)
        )
        conn.commit()

def add_score(user_id, amount):
    cur.execute("UPDATE users SET score = score + ? WHERE user_id=?", (amount, user_id))
    conn.commit()

def sub_score(user_id, amount):
    cur.execute("UPDATE users SET score = score - ? WHERE user_id=?", (amount, user_id))
    conn.commit()
