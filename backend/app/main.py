# backend/app/main.py

from fastapi import FastAPI
from app.gpt_helper import generate_betting_tip
from app.user_data import set_user_favorites, get_user_favorites
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or replace with ["http://localhost:5173"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

class UserPreferences(BaseModel):
    user_id: str
    teams: List[str]

@app.get("/")
def read_root():
    return {"message": "NBA Betting Advisor API is running"}

@app.get("/advise")
def advise(team1: str, team2: str):
    tip = generate_betting_tip(team1, team2)
    return {
        "team_1": team1,
        "team_2": team2,
        "gpt_explanation": tip
    }

@app.post("/set_teams")
def save_favorites(prefs: UserPreferences):
    set_user_favorites(prefs.user_id, prefs.teams)
    return {"message": "Favorite teams saved."}

@app.get("/get_advice")
def advise_favorites(user_id: str):
    teams = get_user_favorites(user_id)
    if len(teams) < 2:
        return {"error": "Please set at least 2 favorite teams."}
    
    team1, team2 = teams[0], teams[1]
    tip = generate_betting_tip(team1, team2)
    return {
        "user_id": user_id,
        "teams_considered": [team1, team2],
        "gpt_betting_tip": tip
    }
