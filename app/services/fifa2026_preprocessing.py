"""
fifa2026_preprocessing.py
Feature engineering and preprocessing for the FIFA 2026 datasets.

Derived features:
  Matches  -> total_goals, goal_diff, is_draw, round_encoded, host_played
  Players  -> goals_per_90, assists_per_90, contributions, efficiency_score
  Teams    -> win_rate, avg_goals_scored, avg_goals_conceded, clean_sheets
  Encoding -> LabelEncoder on Confederation, Position
  Scaling  -> MinMaxScaler on all numeric columns (model-ready output)
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from app.services.fifa2026_loader import (
    load_matches, load_players, load_teams, load_groups
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed', 'fifa2026')
os.makedirs(PROC_DIR, exist_ok=True)

ROUND_ORDER = {
    'Group Stage':   0,
    'Round of 32':   1,
    'Round of 16':   2,
    'Quarter-Final': 3,
    'Semi-Final':    4,
    'Third Place':   5,
    'Final':         6,
}


# ─────────────────────────────────────────────────────────
# MATCHES
# ─────────────────────────────────────────────────────────

def engineer_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns to the matches DataFrame."""
    df = df.copy()
    df['total_goals']   = df['HomeGoals'] + df['AwayGoals']
    df['goal_diff']     = df['HomeGoals'] - df['AwayGoals']
    df['is_draw']       = (df['HomeGoals'] == df['AwayGoals']).astype(int)
    df['round_encoded'] = df['Round'].map(ROUND_ORDER).fillna(-1).astype(int)

    # Host-nation involvement flag
    host_nations = {'United States', 'Canada', 'Mexico'}
    df['host_played'] = (
        df['HomeTeam'].isin(host_nations) | df['AwayTeam'].isin(host_nations)
    ).astype(int)

    # Result label: 0=Away win, 1=Draw, 2=Home win
    conditions = [
        df['HomeGoals'] > df['AwayGoals'],
        df['HomeGoals'] == df['AwayGoals'],
    ]
    df['result_label'] = np.select(conditions, [2, 1], default=0)
    return df


# ─────────────────────────────────────────────────────────
# PLAYERS
# ─────────────────────────────────────────────────────────

def engineer_players(df: pd.DataFrame) -> pd.DataFrame:
    """Add per-90-minute and efficiency features to players DataFrame."""
    df = df.copy()
    mins = df['Minutes'].clip(lower=1)
    df['goals_per_90']    = (df['Goals']   / mins * 90).round(3)
    df['assists_per_90']  = (df['Assists'] / mins * 90).round(3)
    df['contributions']   = df['Goals'] + df['Assists']
    # Efficiency: weighted contribution per 90 mins played
    df['efficiency_score'] = (
        (df['Goals'] * 2 + df['Assists']) / (mins / 90)
    ).round(3)
    # Shot accuracy
    df['shot_accuracy'] = np.where(
        df['Shots'] > 0,
        (df['ShotsOnTarget'] / df['Shots'] * 100).round(1),
        0.0
    )
    # Encode Position
    le = LabelEncoder()
    df['position_encoded'] = le.fit_transform(df['Position'].fillna('Unknown'))
    return df


# ─────────────────────────────────────────────────────────
# TEAMS (aggregated from matches)
# ─────────────────────────────────────────────────────────

def engineer_teams(matches_df: pd.DataFrame, teams_df: pd.DataFrame) -> pd.DataFrame:
    """Compute aggregate match-level team stats and merge into teams DataFrame."""
    df = teams_df.copy()

    records = []
    for nation in df['Nation']:
        home = matches_df[matches_df['HomeTeam'] == nation]
        away = matches_df[matches_df['AwayTeam'] == nation]
        played = len(home) + len(away)
        if played == 0:
            records.append({'Nation': nation, 'Played': 0, 'Wins': 0,
                            'avg_goals_scored': 0.0, 'avg_goals_conceded': 0.0,
                            'win_rate': 0.0, 'clean_sheets': 0})
            continue
        goals_scored    = home['HomeGoals'].sum() + away['AwayGoals'].sum()
        goals_conceded  = home['AwayGoals'].sum() + away['HomeGoals'].sum()
        wins = (
            (home['Winner'] == nation).sum() +
            (away['Winner'] == nation).sum()
        )
        clean = (
            (home['AwayGoals'] == 0).sum() +
            (away['HomeGoals'] == 0).sum()
        )
        records.append({
            'Nation':              nation,
            'Played':              int(played),
            'Wins':                int(wins),
            'avg_goals_scored':    round(goals_scored  / played, 2),
            'avg_goals_conceded':  round(goals_conceded / played, 2),
            'win_rate':            round(wins / played, 3),
            'clean_sheets':        int(clean),
        })

    stats_df = pd.DataFrame(records)
    df = df.merge(stats_df, on='Nation', how='left')

    # Encode Confederation
    le = LabelEncoder()
    df['confederation_encoded'] = le.fit_transform(df['Confederation'].fillna('Unknown'))
    return df


# ─────────────────────────────────────────────────────────
# GROUPS
# ─────────────────────────────────────────────────────────

def engineer_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Add goal-difference rank and points-per-game to group standings."""
    df = df.copy()
    df['points_per_game'] = (df['Points'] / df['Played'].clip(lower=1)).round(2)
    df['gd_positive']     = (df['GD'] > 0).astype(int)
    return df


# ─────────────────────────────────────────────────────────
# NORMALIZATION (MinMax)
# ─────────────────────────────────────────────────────────

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply MinMaxScaler to all numeric columns; return scaled copy."""
    df = df.copy()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    scaler = MinMaxScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df


# ─────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────

def preprocess_all() -> dict:
    """Run full preprocessing pipeline and return engineered DataFrames."""
    # Load cleaned data (fall back to raw if processed not available)
    try:
        matches_df = load_matches(processed=True)
    except FileNotFoundError:
        matches_df = load_matches(processed=False)
    try:
        players_df = load_players(processed=True)
    except FileNotFoundError:
        players_df = load_players(processed=False)
    try:
        teams_df = load_teams(processed=True)
    except FileNotFoundError:
        teams_df = load_teams(processed=False)
    try:
        groups_df = load_groups(processed=True)
    except FileNotFoundError:
        groups_df = load_groups(processed=False)

    matches_eng = engineer_matches(matches_df)
    players_eng = engineer_players(players_df)
    teams_eng   = engineer_teams(matches_df, teams_df)
    groups_eng  = engineer_groups(groups_df)

    print("[Preprocessing] Feature engineering complete.")
    print(f"  Matches columns : {list(matches_eng.columns)}")
    print(f"  Players columns : {list(players_eng.columns)}")
    print(f"  Teams columns   : {list(teams_eng.columns)}")
    print(f"  Groups columns  : {list(groups_eng.columns)}")

    return {
        'matches': matches_eng,
        'players': players_eng,
        'teams':   teams_eng,
        'groups':  groups_eng,
    }


if __name__ == '__main__':
    preprocess_all()
