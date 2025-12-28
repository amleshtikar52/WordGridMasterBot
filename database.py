from collections import defaultdict

scores = defaultdict(int)

def add_score(user_id, points):
    scores[user_id] += points

def remove_score(user_id, points):
    scores[user_id] -= points

def reset_score(user_id):
    scores[user_id] = 0

def get_score(user_id):
    return scores[user_id]

def get_leaderboard(limit=10):
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
