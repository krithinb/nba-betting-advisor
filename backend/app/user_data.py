# backend/app/user_data.py

import redis
import json

# Connect to Redis (running locally)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def set_user_favorites(user_id: str, teams: list[str]) -> None:
    """
    Save a user's favorite teams to Redis.
    """
    redis_client.set(f"user:{user_id}:favorites", json.dumps(teams))

def get_user_favorites(user_id: str) -> list[str]:
    """
    Retrieve a user's favorite teams from Redis.
    Returns an empty list if no data is found.
    """
    data = redis_client.get(f"user:{user_id}:favorites")
    return json.loads(data) if data else []

def cache_betting_tip(team1: str, team2: str, tip: str, ttl_seconds: int = 86400) -> None:
    """
    Cache a betting tip in Redis with a default TTL of 24 hours.
    """
    key = f"betting_tip:{team1.lower()}:{team2.lower()}"
    redis_client.set(key, tip, ex=ttl_seconds)

def get_cached_betting_tip(team1: str, team2: str) -> str | None:
    """
    Retrieve a cached betting tip if available.
    """
    key = f"betting_tip:{team1.lower()}:{team2.lower()}"
    return redis_client.get(key)