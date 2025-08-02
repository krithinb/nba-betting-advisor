import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_betting_tip(team1, team2):
    prompt = f"""
You are a sports betting advisor helping young NBA fans. 
Given a matchup between the {team1} and the {team2}, predict the winner, 
explain your reasoning, and provide a betting recommendation. 
Use a casual tone that still sounds smart and confident.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content