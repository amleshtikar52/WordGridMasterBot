from collections import defaultdict

# Active games
games = {}  # chat_id -> game_data

# Scores
group_scores = defaultdict(lambda: defaultdict(int))
global_scores = defaultdict(int)

# Achievements
achievements = defaultdict(set)


def add_score(chat_id, user_id, points):
    group_scores[chat_id][user_id] += points
    global_scores[user_id] += points


def sub_score(chat_id, user_id, points):
    group_scores[chat_id][user_id] -= points
    global_scores[user_id] -= points


def set_score(chat_id, user_id, value):
    group_scores[chat_id][user_id] = value
    global_scores[user_id] = value
