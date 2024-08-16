import os
import sys
import json
import discord
import uuid
import pandas as pd
import numpy as np
from typing import Final
from yfpy.query import YahooFantasySportsQuery
from dotenv import load_dotenv
from pathlib import Path
from utils.scripts import map_team_key_to_nickname
from joblib import Parallel, delayed

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

    transactions_data = query.get_league_transactions()
    transactions_data = transactions_data.to_json()

    # Load JSON data into Python dictionary
    data = json.loads(transactions_data)

    transactions = data.get()

    return None

def get_playoff_odds():
    """
    Calculates individual team's odds of making the playoffs using
    Monte Carlo simulations

    Parameters
    ----------
    None

    Returns
    -------
    discord.Embed
        A discord Embed object containing formatted playoff odds
    """
    # Embed structure
    embed = discord.Embed(title="Playoff Odds", color=0x00ff00)

    # Get current week
    current_week = get_current_week()

    # Initialize an empty list to store records
    records = []

    for i in range(1, 15): # the 7 will be eventually replacted by current_week
        # Query data from yahoo
        matchups = query.get_league_matchups_by_week(i)
        # Loop through matchup data
        for i in range(len(matchups)):
            matchup = matchups[i].to_json() # matchup[i] is a yfpy object
            matchup_dict = json.loads(matchup)
            
            # Generate a unique matchup_id (UUID)
            matchup_id = str(uuid.uuid4())

            # Extract information for each team in the matchup
            for team in matchup_dict.get('teams', []):
                team_info = team.get('team', {})
                record = {
                    'matchup_id': matchup_id,
                    'week': matchup_dict.get('week'),
                    'winner_team_key': matchup_dict.get('winner_team_key'),
                    'team_key': team_info.get('team_key'),
                    'team_total_points': team_info.get('team_points', {}).get('total'),
                }
                
                # Add the record to the list
                records.append(record)

    # Convert the list of records to a DataFrame
    df = pd.DataFrame(records)
    # Creating win column 
    df["win"] = np.where(df['winner_team_key'] == df['team_key'], 1, 0)
    
    # Calculate average points and standard deviation for each team
    team_stats = df[df['week'] <= current_week].groupby('team_key').agg({
        'team_total_points': ['mean', 'std', 'sum'],
        'win': 'sum' 
    }).reset_index()

    # Set column names
    team_stats.columns = ['team_key', 'avg_points', 'std_points', 'total_points', 'wins']
    
    ##########################################
    ### Monte Carlo simulations start here ###
    ##########################################

    # Parameters
    n_simulations = 10000                 # Number of Monte Carlo simulations
    n_weeks_remaining = 14 - current_week # Number of weeks remaining in the season
    n_playoff_teams = 8                   # Number of teams that make the playoffs

    def simulate_season(seed):
        # Reproducibility
        np.random.seed(seed)
        # Simulate remainder of season
        for _ in range(n_simulations):
            # df to simulate each team's season
            team_simulation = team_stats[['team_key']].copy()
            team_simulation['wins'] = team_stats['wins'].copy()
            team_simulation['total_points'] = team_stats['total_points'].copy()

            for week in range(n_weeks_remaining):
                # Simulate points for each team
                simulated_points = np.random.normal(
                    team_stats['avg_points'],
                    team_stats['std_points']
                )
                # Simulate matchups based on real schedule
                for idx, row in df[df['week'] == current_week + week].iterrows():
                    team1 = row['team_key']
                    team2 = df[(df['week'] == row['week']) & (df['matchup_id'] == row['matchup_id']) & (df['team_key'] != team1)]['team_key'].values[0]
                    
                    points_team1 = simulated_points[team_stats[team_stats['team_key'] == team1].index[0]]
                    points_team2 = simulated_points[team_stats[team_stats['team_key'] == team2].index[0]]
                    
                    if points_team1 > points_team2:
                        team_simulation.loc[team_simulation['team_key'] == team1, 'wins'] += 1
                    else:
                        team_simulation.loc[team_simulation['team_key'] == team2, 'wins'] += 1
                    
                    team_simulation.loc[team_simulation['team_key'] == team1, 'total_points'] += points_team1
                    team_simulation.loc[team_simulation['team_key'] == team2, 'total_points'] += points_team2
            
            # Sort teams first by wins, then by total points for tie-breaking
            team_simulation = team_simulation.sort_values(by=['wins', 'total_points'], ascending=[False, False])
            
            # Select top N teams for playoffs
            playoff_teams = team_simulation.head(n_playoff_teams)['team_key'].values
            return playoff_teams
    
    # Run simulations in parallel
    results = Parallel(n_jobs=-1)(delayed(simulate_season)(seed) for seed in range(n_simulations))
    # Count playoff appearances for each team
    playoff_counts = pd.Series(np.concatenate(results)).value_counts()
    # Calculate the playoff odds as a percentage
    team_stats['playoff_odds'] = (playoff_counts / n_simulations * 100).reindex(team_stats['team_key']).fillna(0).values
    # Final table for embed
    odds_df = pd.DataFrame()
    odds_df['team_key'] = team_stats['team_key']
    odds_df['playoff_odds'] = team_stats['playoff_odds']
    odds_df = map_team_key_to_nickname(odds_df, 'team_key')
    odds_df = odds_df.sort_values(by='playoff_odds', ascending=False).reset_index(drop=True)

    # Iterate to collect data from embed
    manager_col = "\n".join([f"{row['nickname']}" for _, row in odds_df.iterrows()])
    odds_col = "\n".join([f"{row['playoff_odds']:.2f}" for _, row in odds_df.iterrows()])

    # Adding the table to the embed
    embed.add_field(name="Manager", value=f"```{manager_col}```", inline=True)
    embed.add_field(name="Playoff Odds", value=f"```{odds_col}```", inline=True)

    return embed


def get_power_rankings():
    """
    Calculates individual team's power rankings using the following formula:
    ((avg. score x 6) + [(highest score + lowest score) x 2] + [(winnnig % x 200) x 2]) / 10

    Parameters
    ----------
    None

    Returns
    -------
    discord.Embed
        A discord Embed object containing formatted power rankings
    """
    # Embed structure
    embed = discord.Embed(title="Richie's Power Rankings", color=0x00ff00)
    # Get current week
    current_week = get_current_week()

    # Initialize an empty list to store records
    records = []

    for i in range(1, current_week + 1): 
        # Query data from yahoo
        matchups = query.get_league_matchups_by_week(i)
        # Loop through matchup data
        for i in range(len(matchups)):
            matchup = matchups[i].to_json() # matchup[i] is a yfpy object
            matchup_dict = json.loads(matchup)
            
            # Generate a unique matchup_id (UUID)
            matchup_id = str(uuid.uuid4())

            # Extract information for each team in the matchup
            for team in matchup_dict.get('teams', []):
                team_info = team.get('team', {})
                record = {
                    'matchup_id': matchup_id,
                    'week': matchup_dict.get('week'),
                    'winner_team_key': matchup_dict.get('winner_team_key'),
                    'team_key': team_info.get('team_key'),
                    'team_total_points': team_info.get('team_points', {}).get('total'),
                    'team_projected_points': team_info.get('team_projected_points', {}).get('total')
                }
                
                # Add the record to the list
                records.append(record)

    # Convert the list of records to a DataFrame
    df = pd.DataFrame(records)
    # Creating win column 
    df["win"] = np.where(df['winner_team_key'] == df['team_key'], 1, 0)
    
    # Calculate average points and standard deviation for each team
    team_stats = df.groupby('team_key').agg({
        'team_total_points': ['mean', 'std', 'sum', 'min', 'max'],
        'win': 'sum' 
    }).reset_index()

    # Set column names
    team_stats.columns = ['team_key', 'avg_points', 'std_points', 'total_points', 'max_points', 'min_points', 'wins']
    # Map team key to nickname
    team_stats = map_team_key_to_nickname(team_stats, 'team_key')
    # Calculate ranking
    team_stats['p_rank'] = (
        (team_stats.avg_points * 6) +
        ((team_stats.max_points + team_stats.min_points) * 2) +
        (((team_stats.wins / current_week) * 200) * 2)
    ) / 10
    # grab only rank and nickname
    p_rank_table = pd.DataFrame()
    p_rank_table['Manager'] = team_stats['nickname']
    p_rank_table['Power Score'] = team_stats['p_rank']
   # Add a new 'Rank' column based on the Power Score
    p_rank_table['Rank'] = p_rank_table['Power Score'].rank(ascending=False, method='min').astype(int)
    # Sort by Rank if needed
    p_rank_table = p_rank_table.sort_values('Rank').reset_index(drop=True)
    # Prepare the table content
    rank_col = "\n".join([f"{row['Rank']}" for _, row in p_rank_table.iterrows()])
    manager_col = "\n".join([f"{row['Manager']}" for _, row in p_rank_table.iterrows()])
    score_col = "\n".join([f"{row['Power Score']:.2f}" for _, row in p_rank_table.iterrows()])

    # Adding the table to the embed
    embed.add_field(name="Rank", value=f"```{rank_col}```", inline=True)
    embed.add_field(name="Manager", value=f"```{manager_col}```", inline=True)
    embed.add_field(name="Power Score", value=f"```{score_col}```", inline=True)
    
    return embed


def get_whatif_matrix():
    """
    Creates a matrix displaying each team's record as if 
    they had played every other team's schedule.

    Parameters
    ----------
    None

    Returns
    -------
    discord.Embed
        A discord Embed object containing formatted matrix
    """
    # Embed structure
    embed = discord.Embed(title="Playoff Odds", color=0x00ff00)

    # Get current week
    current_week = get_current_week()

    # Initialize an empty list to store records
    records = []