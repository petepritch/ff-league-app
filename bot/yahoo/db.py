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

transactions_data = query.get_league_transactions()

print(type(transactions_data))