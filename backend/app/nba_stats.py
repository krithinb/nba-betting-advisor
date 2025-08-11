import requests
from datetime import datetime, timedelta

BASE_URL = "https://www.balldontlie.io/api/v1"

def get_team_stats(team_name: str):
    # Step 1: Match team name or abbreviation
    resp = requests.get(f"{BASE_URL}/teams")
    if resp.status_code != 200:
        print("Error fetching teams:", resp.status_code)
        return None
    teams = resp.json().get("data", [])

    normalized = team_name.lower()
    matched = next(
        (t for t in teams if normalized in t["full_name"].lower() or normalized == t["abbreviation"].lower()), None
    )
    if not matched:
        print(f"Team '{team_name}' not found.")
        return None
    team_id, name, abbr = matched["id"], matched["full_name"], matched["abbreviation"]

    # Step 2: Fetch last 5 recent regular season games
    end = datetime.now()
    start = end - timedelta(days=60)
    games_resp = requests.get(
        f"{BASE_URL}/games",
        params={
            "team_ids[]": team_id,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "per_page": 100
        }
    )
    if games_resp.status_code != 200:
        print(f"Error fetching games for {team_name}: {games_resp.status_code}")
        return None
    games = [g for g in games_resp.json().get("data", []) if not g.get("postseason")]
    recent = games[:5]
    if not recent:
        print(f"No recent games found for {team_name}")
        return None

    wins = pts_for = pts_against = 0
    for g in recent:
        home = g["home_team"]["id"] == team_id
        team_score = g["home_team_score"] if home else g["visitor_team_score"]
        opp_score = g["visitor_team_score"] if home else g["home_team_score"]
        pts_for += team_score
        pts_against += opp_score
        wins += team_score > opp_score

    avg_sf = round(pts_for / len(recent), 1)
    avg_sa = round(pts_against / len(recent), 1)
    win_pct = round((wins / len(recent)) * 100, 1)

    return {
        "team_name": name,
        "team_id": team_id,
        "abbreviation": abbr,
        "avg_points_scored": avg_sf,
        "avg_points_allowed": avg_sa,
        "win_rate": win_pct
    }

def get_betting_odds():
    # No external odds integration—stats are used to infer advice instead
    return None
