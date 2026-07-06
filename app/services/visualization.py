import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from app.services.loader import load_players, load_teams, load_matches, load_standings

# Use non-interactive backend for server environments
matplotlib.use('Agg')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHARTS_DIR = os.path.join(BASE_DIR, 'static', 'images', 'charts')

def ensure_charts_dir():
    os.makedirs(CHARTS_DIR, exist_ok=True)

def generate_top_scorers_chart():
    ensure_charts_dir()
    players_df = load_players(processed=True)
    
    top_scorers = players_df.sort_values(by='Goals', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Goals', y='Name', data=top_scorers, palette='viridis')
    plt.title('Top 10 Goal Scorers', fontsize=16)
    plt.xlabel('Goals', fontsize=12)
    plt.ylabel('Player', fontsize=12)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, 'top_scorers.png')
    plt.savefig(filepath)
    plt.close()
    
    return 'images/charts/top_scorers.png'

def generate_team_points_chart():
    ensure_charts_dir()
    standings_df = load_standings(processed=True)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Team', y='Points', data=standings_df, palette='mako')
    plt.title('League Standings - Points', fontsize=16)
    plt.xlabel('Team', fontsize=12)
    plt.ylabel('Points', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, 'team_points.png')
    plt.savefig(filepath)
    plt.close()
    
    return 'images/charts/team_points.png'

def generate_goals_distribution_chart():
    ensure_charts_dir()
    matches_df = load_matches(processed=True)
    
    # Calculate total goals per match
    total_goals = matches_df['HomeGoals'] + matches_df['AwayGoals']
    
    plt.figure(figsize=(8, 6))
    sns.histplot(total_goals, bins=range(0, 10), kde=True, color='blue')
    plt.title('Distribution of Goals Per Match', fontsize=16)
    plt.xlabel('Total Goals', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, 'goals_distribution.png')
    plt.savefig(filepath)
    plt.close()
    
    return 'images/charts/goals_distribution.png'

def generate_all_charts():
    """
    Generate all charts used in the dashboard.
    """
    paths = {
        'top_scorers': generate_top_scorers_chart(),
        'team_points': generate_team_points_chart(),
        'goals_distribution': generate_goals_distribution_chart()
    }
    return paths
