# backend/app/user_data.py

user_teams = {}

def set_favorite_teams(user_id: str, teams: list):
    user_teams[user_id] = teams

def get_favorite_teams(user_id: str):
    return user_teams.get(user_id, [])
