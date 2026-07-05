import os
import pandas as pd

# Define paths relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def get_csv_path(filename, processed=False):
    """
    Get the absolute path of a dataset file.
    """
    directory = PROCESSED_DATA_DIR if processed else RAW_DATA_DIR
    return os.path.join(directory, filename)

def load_dataset(filename, processed=False):
    """
    Load a CSV file into a pandas DataFrame.
    """
    path = get_csv_path(filename, processed)
    if not os.path.exists(path):
        # Fallback to raw if processed file is requested but doesn't exist yet
        if processed:
            path = get_csv_path(filename, processed=False)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset file not found at: {path}")
            
    return pd.read_csv(path)

def load_teams(processed=False):
    """
    Load teams dataset.
    """
    return load_dataset('teams.csv', processed)

def load_players(processed=False):
    """
    Load players dataset.
    """
    return load_dataset('players.csv', processed)

def load_matches(processed=False):
    """
    Load matches dataset.
    """
    return load_dataset('matches.csv', processed)

def load_standings(processed=False):
    """
    Load standings dataset.
    """
    return load_dataset('standings.csv', processed)
