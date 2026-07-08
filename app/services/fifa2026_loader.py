"""
fifa2026_loader.py
Loads FIFA World Cup 2026 raw and processed CSV datasets into Pandas DataFrames.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR  = os.path.join(BASE_DIR, 'data', 'raw',       'fifa2026')
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed',  'fifa2026')

_FILE_MAP = {
    'matches': 'wc2026_matches.csv',
    'players': 'wc2026_players.csv',
    'teams':   'wc2026_teams.csv',
    'groups':  'wc2026_groups.csv',
}


def _load(name: str, processed: bool = False) -> pd.DataFrame:
    base = PROC_DIR if processed else RAW_DIR
    path = os.path.join(base, _FILE_MAP[name])
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)


def load_matches(processed: bool = False) -> pd.DataFrame:
    """Return the matches DataFrame (104 rows)."""
    return _load('matches', processed)


def load_players(processed: bool = False) -> pd.DataFrame:
    """Return the players DataFrame (192 rows)."""
    return _load('players', processed)


def load_teams(processed: bool = False) -> pd.DataFrame:
    """Return the teams DataFrame (48 rows)."""
    return _load('teams', processed)


def load_groups(processed: bool = False) -> pd.DataFrame:
    """Return the group-stage standings DataFrame (48 rows)."""
    return _load('groups', processed)


def load_all(processed: bool = False) -> dict:
    """Load all four datasets and return as a dict."""
    return {
        'matches': load_matches(processed),
        'players': load_players(processed),
        'teams':   load_teams(processed),
        'groups':  load_groups(processed),
    }
