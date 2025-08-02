from fastapi import FastAPI
from app.gpt_helper import generate_betting_tip
from app.user_data import set_favorite_teams, get_favorite_teams
from typing import List
from pydantic import BaseModel

app = FastAPI()

class UserPreferences(BaseModel):
    user_id: str
    teams: List[str]

@app.get("/")
def read_root():
    return {"message": "NBA Matchup Predictor API is running"}

@app.get("/advise")
def advise(team1: str, team2: str):
    summary = generate_betting_tip(team1, team2)
    return {
        "team_1": team1,
        "team_2": team2,
        "gpt_explanation": summary
    }

@app.post("/set_teams")
def save_favorites(prefs: UserPreferences):
    set_favorite_teams(prefs.user_id, prefs.teams)
    return {"message": "Favorite teams saved."}

@app.get("/get_advice")
def advise_favorites(user_id: str):
    teams = get_favorite_teams(user_id)
    if len(teams) < 2:
        return {"error": "Please set at least 2 favorite teams."}
    
    team1, team2 = teams[0], teams[1]
    tip = generate_betting_tip(team1, team2)
    return {
        "user_id": user_id,
        "teams_considered": [team1, team2],
        "gpt_betting_tip": tip
    }