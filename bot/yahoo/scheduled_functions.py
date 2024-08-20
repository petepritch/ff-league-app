import os
import sys
import json
from typing import Final
from yfpy.query import YahooFantasySportsQuery
from dotenv import load_dotenv
from pathlib import Path
from functionality import get_current_week

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
####################################################
### YAHOO FANTASY SPORTS API SCHEDULED FUNCTIONS ###
####################################################

def get_power_rankings():
    """
    This function returns the power rankings of the teams in the league for a given week,
    along with the change in the power rankings from the previous week. The power rankings
    are determined by the following equation:

    Power rankings are then delivered by Marcy with commentary developed by Llamma.cpp, and 
    trained on ESPN, CBS, and The Atheletic NFL power rankings articles along with previous
    group chat data. 
    
    Parameters
    ----------
    data
        json formatted string of

    Returns
    -------
    string
        formatted for discord chat
    """
    
    current_week = get_current_week()

    for i in range(1, current_week + 1):
        matchups_data = query.get_league_matchups_by_week(i).to_json()
        data = json.dumps(matchups_data)

        teams = data.get('teams', [])
        for team_info in teams:
            team = team_info.get('team', {})

            



    p_rank_up_emoji = "🟢"
    p_rank_down_emoji = "🔻"
    p_rank_same_emoji = "🟰"

    return 

get_power_rankings()