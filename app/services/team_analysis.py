import pandas as pd
from app.services.loader import load_matches, load_teams

def compare_teams(team_a_name, team_b_name):
    """
    Compare two teams based on head-to-head and overall season stats.
    """
    matches_df = load_matches(processed=True)
    teams_df = load_teams(processed=True)
    
    # Head to head matches
    h2h_matches = matches_df[((matches_df['HomeTeam'] == team_a_name) & (matches_df['AwayTeam'] == team_b_name)) |
                             ((matches_df['HomeTeam'] == team_b_name) & (matches_df['AwayTeam'] == team_a_name))]
                             
    team_a_wins = len(h2h_matches[h2h_matches['Winner'] == team_a_name])
    team_b_wins = len(h2h_matches[h2h_matches['Winner'] == team_b_name])
    draws = len(h2h_matches[h2h_matches['Winner'] == 'Draw'])
    
    # Calculate home vs away advantage for a given team
    def get_home_away_stats(team_name):
        home_matches = matches_df[matches_df['HomeTeam'] == team_name]
        away_matches = matches_df[matches_df['AwayTeam'] == team_name]
        
        home_wins = len(home_matches[home_matches['Winner'] == team_name])
        away_wins = len(away_matches[away_matches['Winner'] == team_name])
        
        return {
            'home_win_rate': (home_wins / len(home_matches) * 100) if len(home_matches) > 0 else 0.0,
            'away_win_rate': (away_wins / len(away_matches) * 100) if len(away_matches) > 0 else 0.0
        }
        
    team_a_context = get_home_away_stats(team_a_name)
    team_b_context = get_home_away_stats(team_b_name)
    
    return {
        'h2h': {
            'total_matches': len(h2h_matches),
            f'{team_a_name}_wins': team_a_wins,
            f'{team_b_name}_wins': team_b_wins,
            'draws': draws
        },
        'context': {
            team_a_name: team_a_context,
            team_b_name: team_b_context
        }
    }

def team_performance_trend(team_name):
    """
    Get a time series of a team's performance (points over time).
    """
    matches_df = load_matches(processed=True)
    matches_df = matches_df.sort_values(by='Date')
    
    team_matches = matches_df[(matches_df['HomeTeam'] == team_name) | (matches_df['AwayTeam'] == team_name)]
    
    cumulative_points = 0
    trend = []
    
    for idx, match in team_matches.iterrows():
        if match['Winner'] == team_name:
            cumulative_points += 3
            result = 'W'
        elif match['Winner'] == 'Draw':
            cumulative_points += 1
            result = 'D'
        else:
            result = 'L'
            
        trend.append({
            'date': match['Date'],
            'opponent': match['AwayTeam'] if match['HomeTeam'] == team_name else match['HomeTeam'],
            'result': result,
            'cumulative_points': cumulative_points
        })
        
    return trend
