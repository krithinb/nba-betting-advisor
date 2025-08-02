import requests

# API Key from Odds API
API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key from OddsAPI

# Set the sport to 'basketball_nba' and configure your region, markets, and other parameters
SPORT = 'basketball_nba'
REGIONS = 'us'  # US betting markets
MARKETS = 'h2h,spreads'  # Moneyline (h2h) and Spread (spreads)
ODDS_FORMAT = 'decimal'  # Decimal odds format
DATE_FORMAT = 'iso'  # ISO date format

# Get a list of sports available
def get_sports():
    sports_url = f'https://api.the-odds-api.com/v4/sports'
    response = requests.get(sports_url, params={'api_key': API_KEY})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching sports data: {response.status_code}")
        return None

# Fetch odds for NBA matchups
def get_betting_odds():
    # Requesting the odds for upcoming NBA games
    odds_url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'
    response = requests.get(
        odds_url,
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )
    
    if response.status_code == 200:
        odds_data = response.json()
        return odds_data
    else:
        print(f"Error fetching odds: {response.status_code}")
        return None

# Fetch specific team stats for a matchup
def get_team_stats(team_name):
    # Get the list of all teams from the NBA API
    teams_url = "https://www.balldontlie.io/api/v1/teams"
    response = requests.get(teams_url)
    
    if response.status_code != 200:
        print(f"Error fetching teams: {response.status_code}")
        return None
    
    teams_data = response.json()["data"]
    
    team = next((t for t in teams_data if t['full_name'].lower() == team_name.lower()), None)
    
    if team:
        team_stats = {
            'team_name': team['full_name'],
            'team_id': team['id'],
            'abbreviation': team['abbreviation']
        }
        return team_stats
    else:
        print(f"Team {team_name} not found.")
        return None

