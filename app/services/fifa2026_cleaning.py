"""
fifa2026_cleaning.py
Data cleaning pipeline for the FIFA World Cup 2026 datasets.

Steps applied to every DataFrame:
  1. Drop exact duplicate rows
  2. Strip leading/trailing whitespace from string columns
  3. Fill missing numeric values with column median
  4. Fill missing categorical values with column mode
  5. Convert Date column to datetime
  6. Validate goal values (must be >= 0)
  7. Remove extreme attendance outliers (IQR method)
  8. Save cleaned data to data/processed/fifa2026/
"""

import os
import pandas as pd
import numpy as np

from app.services.fifa2026_loader import (
    load_matches, load_players, load_teams, load_groups
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC_DIR = os.path.join(BASE_DIR, 'data', 'processed', 'fifa2026')
os.makedirs(PROC_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────
# GENERIC HELPERS
# ─────────────────────────────────────────────────────────

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows and reset the index."""
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removed = before - len(df)
    if removed:
        print(f"  [clean] Dropped {removed} duplicate row(s).")
    return df


def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from all object/string columns."""
    str_cols = df.select_dtypes(include=['object', 'str']).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
    return df


def fill_missing_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Fill NaN in numeric columns with the column median."""
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        n_missing = df[col].isna().sum()
        if n_missing:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  [clean] Filled {n_missing} NaN(s) in '{col}' with median={median_val:.2f}.")
    return df


def fill_missing_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """Fill NaN in categorical/string columns with the column mode."""
    cat_cols = df.select_dtypes(include=['object', 'str']).columns
    for col in cat_cols:
        n_missing = df[col].isna().sum()
        if n_missing:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            print(f"  [clean] Filled {n_missing} NaN(s) in '{col}' with mode='{mode_val}'.")
    return df


def convert_dates(df: pd.DataFrame, col: str = 'Date') -> pd.DataFrame:
    """Convert a string date column to datetime dtype."""
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


def validate_goals(df: pd.DataFrame) -> pd.DataFrame:
    """Clip any negative goal values to 0 and report them."""
    for col in ['HomeGoals', 'AwayGoals']:
        if col in df.columns:
            neg = (df[col] < 0).sum()
            if neg:
                print(f"  [clean] Fixed {neg} negative value(s) in '{col}'.")
            df[col] = df[col].clip(lower=0)
    return df


def remove_outliers_iqr(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Remove rows where col is beyond 3 * IQR from Q1/Q3."""
    if col not in df.columns:
        return df
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 3 * IQR, Q3 + 3 * IQR
    before = len(df)
    df = df[(df[col] >= lower) & (df[col] <= upper)].reset_index(drop=True)
    removed = before - len(df)
    if removed:
        print(f"  [clean] Removed {removed} outlier row(s) in '{col}'.")
    return df


def _save(df: pd.DataFrame, filename: str) -> None:
    path = os.path.join(PROC_DIR, filename)
    df.to_csv(path, index=False)
    print(f"  [save]  {filename} -> {len(df)} rows saved.")


# ─────────────────────────────────────────────────────────
# DATASET-SPECIFIC CLEANERS
# ─────────────────────────────────────────────────────────

def clean_matches() -> pd.DataFrame:
    """Clean the matches dataset and save to processed/."""
    print("\n[Cleaning] wc2026_matches ...")
    df = load_matches(processed=False)
    df = drop_duplicates(df)
    df = strip_strings(df)
    df = convert_dates(df, 'Date')
    df = fill_missing_numeric(df)
    df = fill_missing_categorical(df)
    df = validate_goals(df)
    df = remove_outliers_iqr(df, 'Attendance')
    _save(df, 'wc2026_matches.csv')
    return df


def clean_players() -> pd.DataFrame:
    """Clean the players dataset and save to processed/."""
    print("\n[Cleaning] wc2026_players ...")
    df = load_players(processed=False)
    df = drop_duplicates(df)
    df = strip_strings(df)
    df = fill_missing_numeric(df)
    df = fill_missing_categorical(df)
    # Goals and assists must be non-negative integers
    for col in ['Goals', 'Assists', 'YellowCards', 'RedCards']:
        if col in df.columns:
            df[col] = df[col].clip(lower=0).astype(int)
    df = remove_outliers_iqr(df, 'Minutes')
    _save(df, 'wc2026_players.csv')
    return df


def clean_teams() -> pd.DataFrame:
    """Clean the teams dataset and save to processed/."""
    print("\n[Cleaning] wc2026_teams ...")
    df = load_teams(processed=False)
    df = drop_duplicates(df)
    df = strip_strings(df)
    df = fill_missing_numeric(df)
    df = fill_missing_categorical(df)
    _save(df, 'wc2026_teams.csv')
    return df


def clean_groups() -> pd.DataFrame:
    """Clean the group-stage standings dataset and save to processed/."""
    print("\n[Cleaning] wc2026_groups ...")
    df = load_groups(processed=False)
    df = drop_duplicates(df)
    df = strip_strings(df)
    df = fill_missing_numeric(df)
    df = fill_missing_categorical(df)
    for col in ['Won', 'Drawn', 'Lost', 'GF', 'GA', 'Points']:
        if col in df.columns:
            df[col] = df[col].clip(lower=0).astype(int)
    _save(df, 'wc2026_groups.csv')
    return df


def clean_all() -> dict:
    """Run all cleaning pipelines and return a dict of cleaned DataFrames."""
    return {
        'matches': clean_matches(),
        'players': clean_players(),
        'teams':   clean_teams(),
        'groups':  clean_groups(),
    }


if __name__ == '__main__':
    clean_all()
    print("\n[Done] All FIFA 2026 datasets cleaned and saved.")
