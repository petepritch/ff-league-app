import os
import sys
import json
import pandas as pd
import discord
from typing import Final
from yfpy.query import YahooFantasySportsQuery
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine

"""
THIS FILE CONTAINS GENERIC PYTHON FUNCTIONS THAT 
CAN BE USED ACCROSS THE ENTIRE REPOSITORY 
"""

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

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def map_team_key_to_nickname(df: pd.DataFrame, key: str) -> pd.DataFrame:
    """
    
    """

    # Query manager data 
    managers = query.get_league_teams()
    # Initialize space to hold data
    records = []

    for i in range(len(managers)):
        manager = managers[i].to_json()
        manager_dict = json.loads(manager)
        record = {
            'team_key': manager_dict.get('team_key'),
            'nickname': manager_dict.get("managers", {}).get("manager", {}).get("nickname"),
        }

        records.append(record)
        
    # Convert the list of records to a DataFrame
    df2 = pd.DataFrame(records)
    # Merge data
    df_merged = pd.merge(df, df2, on=key, how='left')

    return df_merged