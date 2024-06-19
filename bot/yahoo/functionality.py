import os
import sys
import json
from yfpy.models import Standings
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
    Gets the current matchup scores

    Paramaters
    ----------
    None

    Returns
    -------
    dictionary

    """
    week = get_current_week()
    return

def get_standings(data):
    """
    Gets league standings and other information

    Parameters
    ----------
    None

    Returns
    -------
    
    """
    output = []
    
    # Load JSON data into a Python dictionary
    data = json.loads(data)
    
    # Header for the table
    output.append("Rank\tNickname\tWins\tLosses\tTotal")
    
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
        clinched_playoffs = team.get('team', {}).get('clinched_playoffs')

        # Determine if the team is in the bottom 4 ranks
        is_bottom_4 = rank is not None and rank >= 9
        is_clinched_playoffs = clinched_playoffs is not None and clinched_playoffs == 1
        
        # Emoji representation
        playoffs_emoji = " ⭐️" if is_clinched_playoffs else ""
        rank_emoji = "💩" if is_bottom_4 else ""
        
        # Format the output string for each team
        if all(x is not None for x in [rank, nickname, wins, losses, total]):
            output.append(f"{rank}\t{nickname}{playoffs_emoji}{rank_emoji}\t{wins}\t{losses}\t{total}")
    
    # Join the list into a single string with newline separation
    return "\n".join(output)

def get_power_rankings(data):
    """
    This function returns the power rankings of the teams in the league for a given week,
    along with the change in the power rankings from the previous week. The power rankings
    are determined
    
    Parameters
    ----------
    data
        json formatted string of

    Returns
    -------
    string
        formatted for discord chat
    """
    
    output = []
    data = json.loads(data)

    # Header for the table 
    output.append("Rank\tNickname\tChange")

    # 
    p_rank_up_emoji = "🟢"
    p_rank_down_emoji = "🔻"
    p_rank_same_emoji = "🟰"

    return None