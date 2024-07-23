import os
import sys
import json
import discord
import pandas as pd
from typing import Final
from yfpy.query import YahooFantasySportsQuery
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

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

# Example with PostgreSQL
DATABASE_URL = "postgresql+psycopg2://user:password@localhost/fantasy_football"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

def get_yahoo_query(league_id, game_id):
    return YahooFantasySportsQuery(
        auth_dir,
        league_id=league_id,
        game_id=game_id,
        game_code='nfl',
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET
    )

def fetch_league_data(query, year):
    
    league_meta = query.get_league_metadata()
    standings = query.get_league_standings()
    scoreboard = query.get_league_standings_by_week(league_meta.current_week)

    # Convert to DataFrame or other structures as needed
    standings_df = pd.json_normalize(standings.to_dict())
    scoreboard_df = pd.json_normalize(scoreboard.to_dict())
    
    return standings_df, scoreboard_df

standings_table = Table('standings', metadata,
    Column('id', Integer, primary_key=True),
    Column('rank', Integer),
    Column('nickname', String),
    Column('wins', Integer),
    Column('losses', Integer),
    Column('points_for', Float),
    Column('points_against', Float),
    Column('year', Integer),
)

scoreboard_table = Table('scoreboard', metadata,
    Column('id', Integer, primary_key=True),
    Column('team1', String),
    Column('team1_score', Float),
    Column('team2', String),
    Column('team2_score', Float),
    Column('week', Integer),
    Column('year', Integer),
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def insert_data(session, standings_df, scoreboard_df, year):
    standings_df['year'] = year
    scoreboard_df['year'] = year
    
    # Insert standings data
    standings_df.to_sql('standings', engine, if_exists='append', index=False)
    
    # Insert scoreboard data
    scoreboard_df.to_sql('scoreboard', engine, if_exists='append', index=False)

def main():
    league_id = '49754'  # Replace with your league ID
    for year in range(2012, 2024):  # Adjust the range for your years
        game_id = get_game_id_for_year(year)  # Define this function based on your game IDs
        query = get_yahoo_query(league_id, game_id)
        standings_df, scoreboard_df = fetch_league_data(query, year)
        insert_data(session, standings_df, scoreboard_df, year)
        
    session.commit()
    session.close()

if __name__ == "__main__":
    main()