import pandas as pd
from app.services.loader import load_players

def compare_players(player_a_id, player_b_id):
    """
    Compare two players side by side.
    """
    players_df = load_players(processed=True)
    
    player_a_data = players_df[players_df['PlayerID'] == player_a_id]
    player_b_data = players_df[players_df['PlayerID'] == player_b_id]
    
    if player_a_data.empty or player_b_data.empty:
        return None
        
    player_a = player_a_data.iloc[0].to_dict()
    player_b = player_b_data.iloc[0].to_dict()
    
    return {
        'player_a': player_a,
        'player_b': player_b
    }

def get_player_efficiency():
    """
    Calculate player efficiency (Goals + Assists per 90 mins).
    """
    players_df = load_players(processed=True)
    
    def calc_efficiency(row):
        mins = row['Minutes Played']
        if mins > 0:
            contributions = row['Goals'] + row['Assists']
            return round((contributions / mins) * 90, 2)
        return 0.0
        
    players_df['Efficiency_Per_90'] = players_df.apply(calc_efficiency, axis=1)
    return players_df.sort_values(by='Efficiency_Per_90', ascending=False)
