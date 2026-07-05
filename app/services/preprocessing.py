import os
import pandas as pd
from app.services.loader import load_teams, load_players, load_matches, load_standings, PROCESSED_DATA_DIR

def clean_teams(df):
    """
    Clean teams dataset.
    """
    df = df.copy()
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    
    # Remove duplicates based on TeamID
    df = df.drop_duplicates(subset=['TeamID'])
    
    # Fill missing values
    df['Founded'] = pd.to_numeric(df['Founded'], errors='coerce').fillna(1900).astype(int)
    df['Capacity'] = pd.to_numeric(df['Capacity'], errors='coerce').fillna(0).astype(int)
    
    return df

def clean_players(df):
    """
    Clean players dataset.
    """
    df = df.copy()
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Remove duplicates based on PlayerID
    df = df.drop_duplicates(subset=['PlayerID'])
    
    # Fill missing values for numerical fields
    numeric_cols_ints = ['Goals', 'Assists', 'Yellow Cards', 'Red Cards', 'Matches Played', 'Minutes Played', 'Age']
    for col in numeric_cols_ints:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    # Rating is a float
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(6.0).astype(float)
    
    # Capitalize position values
    df['Position'] = df['Position'].str.capitalize()
    
    return df

def clean_matches(df):
    """
    Clean matches dataset.
    """
    df = df.copy()
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Remove duplicates based on MatchID
    df = df.drop_duplicates(subset=['MatchID'])
    
    # Convert dates to YYYY-MM-DD
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['Date'] = df['Date'].fillna('2026-01-01')
    
    # Fill numerical fields
    numeric_cols = [
        'HomeGoals', 'AwayGoals', 'HomePossession', 'AwayPossession',
        'HomeShots', 'AwayShots', 'HomeShotsOnTarget', 'AwayShotsOnTarget',
        'HomeCorners', 'AwayCorners', 'HomeYellowCards', 'AwayYellowCards',
        'HomeRedCards', 'AwayRedCards'
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    # Ensure Winner column is logically consistent
    def derive_winner(row):
        if row['HomeGoals'] > row['AwayGoals']:
            return row['HomeTeam']
        elif row['AwayGoals'] > row['HomeGoals']:
            return row['AwayTeam']
        else:
            return 'Draw'
            
    df['Winner'] = df.apply(derive_winner, axis=1)
    
    return df

def clean_standings(df):
    """
    Clean standings dataset.
    """
    df = df.copy()
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Remove duplicates based on Team
    df = df.drop_duplicates(subset=['Team'])
    
    # Convert numerical columns
    numeric_cols = ['Position', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    # Order by points, GD, GF
    df = df.sort_values(by=['Points', 'GD', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
    df['Position'] = df.index + 1
    
    return df

def preprocess_all():
    """
    Load raw files, clean them, and save them to the processed data folder.
    """
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    # Load raw
    raw_teams = load_teams(processed=False)
    raw_players = load_players(processed=False)
    raw_matches = load_matches(processed=False)
    raw_standings = load_standings(processed=False)
    
    # Clean
    cleaned_teams = clean_teams(raw_teams)
    cleaned_players = clean_players(raw_players)
    cleaned_matches = clean_matches(raw_matches)
    cleaned_standings = clean_standings(raw_standings)
    
    # Save processed
    cleaned_teams.to_csv(os.path.join(PROCESSED_DATA_DIR, 'teams.csv'), index=False)
    cleaned_players.to_csv(os.path.join(PROCESSED_DATA_DIR, 'players.csv'), index=False)
    cleaned_matches.to_csv(os.path.join(PROCESSED_DATA_DIR, 'matches.csv'), index=False)
    cleaned_standings.to_csv(os.path.join(PROCESSED_DATA_DIR, 'standings.csv'), index=False)
    
    print("All datasets preprocessed and saved to processed/ directory.")

if __name__ == '__main__':
    preprocess_all()
