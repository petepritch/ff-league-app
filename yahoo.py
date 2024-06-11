import os
import sys
from logging import DEBUG
from pathlib import Path

from dotenv import load_dotenv

project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

from yfpy import Data
from yfpy.logger import get_logger
from yfpy.query import YahooFantasySportsQuery

### ENV SETUP ###

# load .env file in order to read local environment variables
load_dotenv(dotenv_path=project_dir / "auth" / ".env")

# set directory location of private.json for authentication
auth_dir = project_dir / "auth"

# set target directory for data output
data_dir = Path(__file__).parent / "output"

# create YFPY Data instance for saving/loading data
data = Data(data_dir)

### VAR SETUP ###

# Set desired season
def get_season():
    season = 2023
    return season

season = get_season()

# Set desired week
def get_chosen_week():
    chosen_week = 1
    return chosen_week

chosen_week = get_chosen_week()

# set desired Yahoo Fantasy Sports game code
def get_game_code():
    game_code = "nfl"  
    return game_code


game_code = get_game_code()