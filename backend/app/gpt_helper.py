import os
from openai import OpenAI
from app.nba_stats import get_team_stats
from app.user_data import cache_betting_tip, get_cached_betting_tip

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_betting_tip(team1, team2):
    # Check Redis cache
    cached = get_cached_betting_tip(team1, team2)
    if cached:
        return cached

    # Fetch team stats
    team1_stats = get_team_stats(team1)
    team2_stats = get_team_stats(team2)

    if not team1_stats or not team2_stats:
        return "Could not fetch team stats. Please check team names."

    # Build GPT prompt based on stats only
    prompt = f"""
You are an expert NBA betting advisor for college-aged fans.

Here's a matchup between the {team1_stats['team_name']} and the {team2_stats['team_name']}.

{team1_stats['team_name']} (last 5 games):
- Win rate: {team1_stats['win_rate']}%
- Avg points scored: {team1_stats['avg_points_scored']}
- Avg points allowed: {team1_stats['avg_points_allowed']}

{team2_stats['team_name']} (last 5 games):
- Win rate: {team2_stats['win_rate']}%
- Avg points scored: {team2_stats['avg_points_scored']}
- Avg points allowed: {team2_stats['avg_points_allowed']}

Based on this recent performance data:
1. Which team is more likely to win?
2. What would your betting advice be (moneyline, spread, over/under)?
3. Include your confidence level and short explanation why.

Keep the tone confident but friendly, like you're texting a friend who bets casually.
"""

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    # Cache the result
    cache_betting_tip(team1, team2, result)

    return result
