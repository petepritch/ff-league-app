import os
import sys
import json
import discord
from typing import Final
from yfpy.query import YahooFantasySportsQuery
from dotenv import load_dotenv
from pathlib import Path

# set directory location of private.json for authentication
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))
auth_dir = project_dir / "auth"

# Load environment variables from .env file
load_dotenv()

# Fetch Yahoo API credentials from environment variables
CONSUMER_KEY: Final[str] = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET: Final[str] = os.getenv('CONSUMER_SECRET')
REFRESH_TOKEN: Final[str] = os.getenv('REFRESH_TOKEN')

# Fetch league information
query = YahooFantasySportsQuery(
    auth_dir, 
    league_id='49754', # Fill in league_id
    game_code='nfl',   # Leave this as is
    game_id='423',     # Fill in current game id
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    )
##################################################
### YAHOO FANTASY SPORTS API COMMAND FUNCTIONS ###
##################################################

def get_current_week():
    """
    Gets the current week of the fantasy season

    Parameters
    ----------
    None

    Returns
    -------
    int 
        representing the current week [1,18]
    """
    meta_data = query.get_league_metadata()
    current_week = meta_data.current_week

    return current_week

def get_scoreboard():
    """
    Converts multiple matchups data into Discord Embed object

    Paramaters
    ----------
    None

    Returns
    -------
    discord.Embed
        A Discord Embed object containing the formatting matchups

    """
    embed = discord.Embed(title="League Matchups", color=0x00ff00)

    current_week = get_current_week()
    scoreboard_data = query.get_league_scoreboard_by_week(current_week).to_json()

    # Load JSON data into Python dictionary
    data = json.loads(scoreboard_data)

    # Iterate through each matchup
    matchups = data.get('matchups', [])
    for matchup_info in matchups:
        matchup = matchup_info.get('matchup', {})
        
        teams = matchup.get('teams', [])
        if len(teams) != 2:
            continue
        
        team1 = teams[0].get('team', {})
        team2 = teams[1].get('team', {})
        
        # Extracting necessary fields
        nickname1 = team1.get('managers', {}).get('manager', {}).get('nickname', 'Unknown')
        total1 = team1.get('team_points', {}).get('total', '0')
        nickname2 = team2.get('managers', {}).get('manager', {}).get('nickname', 'Unknown')
        total2 = team2.get('team_points', {}).get('total', '0')
        
        # Add fields to the embed
        embed.add_field(name=f"{nickname1}", value=f"Score: **{total1}**", inline=True)
        embed.add_field(name="vs", value="\u200b", inline=True)  # \u200b is a zero-width space
        embed.add_field(name=f"{nickname2}", value=f"Score: **{total2}**", inline=True)
    
    return embed

def get_standings():
    """
    Converts standings data into a Discord Embed Object

    Parameters
    ----------
    None

    Returns
    -------
    discord.Embed
        A Discord Embed object containing the formatted standings
    """
    embed = discord.Embed(title="League Standings", color=0x00ff00)
    
    standings_data = query.get_league_standings()
    standings_data = standings_data.to_json()

    # Load JSON data into a Python dictionary
    data = json.loads(standings_data)

        # Header for the table
    header = f"{'Rank':<5}{'Manager':<20}{'Wins':<5}{'Losses':<7}{'PF':<10}{'PA':<10}"
    
    # Add the header to the embed
    embed.add_field(name="Standings", value=f"```\n{header}\n```", inline=False)
    
    # Iterate through each team in the "teams" list
    teams = data.get('teams', [])
    for team_info in teams:
        team = team_info.get('team', {})
        
        # Extract relevant fields
        rank = team.get('team_standings', {}).get('rank')
        nickname = team.get('managers', {}).get('manager', {}).get('nickname')
        wins = team.get('team_standings', {}).get('outcome_totals', {}).get('wins')
        losses = team.get('team_standings', {}).get('outcome_totals', {}).get('losses')
        total = team.get('team_points', {}).get('total')
        pa = round(team.get('team_standings', {}).get('points_against'), 2)
        clinched_playoffs = team.get('clinched_playoffs')

        # Determine if the team is in the bottom 4 ranks
        is_bottom_4 = rank is not None and rank >= 9
        is_clinched_playoffs = clinched_playoffs is not None and clinched_playoffs == 1
        
        # Emoji representation
        playoffs_emoji = " ⭐️" if is_clinched_playoffs else ""
        rank_emoji = " 💩" if is_bottom_4 else ""

        # Append emojis to the nickname
        full_nickname = f"{nickname}{playoffs_emoji}{rank_emoji}"
        
        # Format the output string for each team
        if all(x is not None for x in [rank, nickname, wins, losses, total, pa]):
            team_info_str = f"{rank:<5}{full_nickname:<20}{wins:<5}{losses:<7}{total:<10}{pa:<10}"
            embed.add_field(name="\u200b", value=f"```\n{team_info_str}\n```", inline=False)
        
    return embed


def get_transactions():
    """
    Converts transactions data into a Discord Embed Object

    Parameters
    ----------
    None

    Returns
    -------
    discord.Embed
        A Discord Embed object containing the formatted transactions
    """
    embed = discord.Embed(title="New Transaction", color=0x00ff00)
    return None