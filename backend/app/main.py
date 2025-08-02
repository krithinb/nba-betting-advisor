from fastapi import FastAPI
from app.gpt_helper import generate_betting_tip

app = FastAPI()

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