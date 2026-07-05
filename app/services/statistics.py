import pandas as pd
from app.services.loader import load_teams, load_players, load_matches, load_standings

def get_league_summary():
    """
    Get high-level summary statistics of the league.
    """
    matches_df = load_matches(processed=True)
    players_df = load_players(processed=True)
    teams_df = load_teams(processed=True)
    
    total_matches = len(matches_df)
    total_goals = matches_df['HomeGoals'].sum() + matches_df['AwayGoals'].sum()
    avg_goals_per_match = round(total_goals / total_matches, 2) if total_matches > 0 else 0.0
    
    total_cards = matches_df['HomeYellowCards'].sum() + matches_df['AwayYellowCards'].sum() + \
                  matches_df['HomeRedCards'].sum() + matches_df['AwayRedCards'].sum()
                  
    total_players = len(players_df)
    total_teams = len(teams_df)
    
    return {
        'total_matches': total_matches,
        'total_goals': int(total_goals),
        'avg_goals': float(avg_goals_per_match),
        'total_cards': int(total_cards),
        'total_players': int(total_players),
        'total_teams': int(total_teams)
    }

def get_team_stats(team_name):
    """
    Calculate detailed stats for a single team.
    """
    matches_df = load_matches(processed=True)
    players_df = load_players(processed=True)
    
    # Filter matches where the team played
    team_matches = matches_df[(matches_df['HomeTeam'] == team_name) | (matches_df['AwayTeam'] == team_name)]
    total_played = len(team_matches)
    
    if total_played == 0:
        return {
            'played': 0, 'won': 0, 'drawn': 0, 'lost': 0,
            'win_rate': 0.0, 'draw_rate': 0.0, 'loss_rate': 0.0,
            'goals_scored': 0, 'goals_conceded': 0,
            'avg_goals_scored': 0.0, 'avg_goals_conceded': 0.0,
            'avg_possession': 0.0, 'clean_sheets': 0,
            'avg_player_rating': 0.0
        }
        
    wins = len(team_matches[team_matches['Winner'] == team_name])
    draws = len(team_matches[team_matches['Winner'] == 'Draw'])
    losses = total_played - wins - draws
    
    # Calculate goals and possession
    goals_scored = 0
    goals_conceded = 0
    possession_sum = 0
    clean_sheets = 0
    
    for idx, match in team_matches.iterrows():
        if match['HomeTeam'] == team_name:
            goals_scored += match['HomeGoals']
            goals_conceded += match['AwayGoals']
            possession_sum += match['HomePossession']
            if match['AwayGoals'] == 0:
                clean_sheets += 1
        else:
            goals_scored += match['AwayGoals']
            goals_conceded += match['HomeGoals']
            possession_sum += match['AwayPossession']
            if match['HomeGoals'] == 0:
                clean_sheets += 1
                
    # Average player rating for this team
    team_players = players_df[players_df['Club'] == team_name]
    avg_rating = team_players['Rating'].mean() if len(team_players) > 0 else 6.0
    
    return {
        'played': int(total_played),
        'won': int(wins),
        'drawn': int(draws),
        'lost': int(losses),
        'win_rate': round((wins / total_played) * 100, 2),
        'draw_rate': round((draws / total_played) * 100, 2),
        'loss_rate': round((losses / total_played) * 100, 2),
        'goals_scored': int(goals_scored),
        'goals_conceded': int(goals_conceded),
        'avg_goals_scored': round(goals_scored / total_played, 2),
        'avg_goals_conceded': round(goals_conceded / total_played, 2),
        'avg_possession': round(possession_sum / total_played, 2),
        'clean_sheets': int(clean_sheets),
        'avg_player_rating': round(avg_rating, 2)
    }

def get_all_teams_stats():
    """
    Get aggregated stats for all teams as a DataFrame.
    """
    teams_df = load_teams(processed=True)
    stats_list = []
    for name in teams_df['Name']:
        t_stats = get_team_stats(name)
        t_stats['Team'] = name
        stats_list.append(t_stats)
    return pd.DataFrame(stats_list)

def get_top_scorers(limit=10):
    """
    Get top goal scorers in the league.
    """
    players_df = load_players(processed=True)
    top_scorers = players_df.sort_values(by=['Goals', 'Rating'], ascending=[False, False]).head(limit)
    return top_scorers[['Name', 'Club', 'Position', 'Goals', 'Rating']].to_dict(orient='records')

def get_top_assists(limit=10):
    """
    Get top assist providers in the league.
    """
    players_df = load_players(processed=True)
    top_assists = players_df.sort_values(by=['Assists', 'Rating'], ascending=[False, False]).head(limit)
    return top_assists[['Name', 'Club', 'Position', 'Assists', 'Rating']].to_dict(orient='records')

def get_top_players(limit=10):
    """
    Get top rated players.
    """
    players_df = load_players(processed=True)
    top_rated = players_df.sort_values(by=['Rating', 'Goals'], ascending=[False, False]).head(limit)
    return top_rated[['Name', 'Club', 'Position', 'Rating', 'Goals', 'Assists']].to_dict(orient='records')
