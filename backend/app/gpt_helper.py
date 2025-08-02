import os
from openai import OpenAI
from app.nba_stats import get_team_stats, get_betting_odds

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_betting_tip(team1, team2):
    # Get team stats (team performance)
    team1_stats = get_team_stats(team1)
    team2_stats = get_team_stats(team2)
    
    # Get betting odds for moneyline, spread, and over/under
    odds = get_betting_odds()
    
    # Extract odds data
    team1_moneyline = odds[0]['home_team_moneyline']  # Assuming first event in the list
    team2_moneyline = odds[0]['away_team_moneyline']
    team1_spread = odds[0]['home_team_spread']
    team2_spread = odds[0]['away_team_spread']
    over_under = odds[0]['total_points']

    prompt = f"""
    You are an expert NBA betting advisor. 
    Given the following matchup between the {team1} and {team2}:
    
    - {team1} win percentage: {team1_stats['team_name']}
    - {team2} win percentage: {team2_stats['team_name']}
    - {team1} points per game: {team1_stats['team_id']}
    - {team2} points per game: {team2_stats['team_id']}
    
    Betting odds:
    - Moneyline: {team1}: {team1_moneyline}, {team2}: {team2_moneyline}
    - Spread: {team1} {team1_spread}, {team2} {team2_spread}
    - Over/Under: {over_under}
    
    Analyze these odds and stats, and recommend the best betting strategy:
    - Which team do you predict will win?
    - Should bettors bet on the moneyline, spread, or total points?
    - What’s your confidence level in this bet, and why?
    """
    
    # Send the prompt to GPT-3 for the prediction
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
