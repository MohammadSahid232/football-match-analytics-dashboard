"""
fifa2026_eda.py
Exploratory Data Analysis functions for FIFA World Cup 2026 datasets.

Functions:
    get_tournament_summary()      -> dict of 10 headline stats
    get_top_scorers(n)            -> DataFrame sorted by Goals desc
    get_top_assisters(n)          -> DataFrame sorted by Assists desc
    goals_by_round()              -> Series: round -> total_goals
    goals_by_confederation()      -> Series: confederation -> total_goals
    attendance_summary()          -> DataFrame: venue-level stats
    correlation_matrix()          -> DataFrame: numeric correlation
    host_nation_analysis()        -> dict comparing host vs non-host
    red_yellow_analysis()         -> dict card statistics
    group_performance_summary()   -> DataFrame: group-level goal stats
"""

import pandas as pd
import numpy as np

from app.services.fifa2026_loader import (
    load_matches, load_players, load_teams, load_groups
)


def _load_data(processed: bool = True):
    """Load all datasets, falling back to raw if processed not found."""
    def safe_load(fn, proc):
        try:
            return fn(processed=proc)
        except FileNotFoundError:
            return fn(processed=False)

    return (
        safe_load(load_matches, processed),
        safe_load(load_players, processed),
        safe_load(load_teams,   processed),
        safe_load(load_groups,  processed),
    )


# ─────────────────────────────────────────────────────────

def get_tournament_summary() -> dict:
    """Return 10 high-level tournament statistics as a dict."""
    matches, players, teams, groups = _load_data()

    total_goals  = int(matches['HomeGoals'].sum() + matches['AwayGoals'].sum())
    total_matches = len(matches)
    avg_goals    = round(total_goals / max(total_matches, 1), 2)
    max_goals    = int((matches['HomeGoals'] + matches['AwayGoals']).max())
    draws        = int((matches['HomeGoals'] == matches['AwayGoals']).sum())

    # Highest-scoring match
    matches['_total'] = matches['HomeGoals'] + matches['AwayGoals']
    top_match_row = matches.loc[matches['_total'].idxmax()]
    top_match     = f"{top_match_row['HomeTeam']} {top_match_row['HomeGoals']}-{top_match_row['AwayGoals']} {top_match_row['AwayTeam']}"

    top_scorer_row = players.sort_values('Goals', ascending=False).iloc[0]
    top_scorer     = f"{top_scorer_row['Name']} ({int(top_scorer_row['Goals'])} goals)"

    total_yc  = int(matches['HomeYellowCards'].sum() + matches['AwayYellowCards'].sum())
    total_rc  = int(matches['HomeRedCards'].sum()    + matches['AwayRedCards'].sum())
    avg_att   = round(matches['Attendance'].mean(), 0)

    return {
        'total_matches':       total_matches,
        'total_goals':         total_goals,
        'avg_goals_per_match': avg_goals,
        'highest_match_goals': max_goals,
        'draws':               draws,
        'highest_scoring_match': top_match,
        'top_scorer':          top_scorer,
        'total_yellow_cards':  total_yc,
        'total_red_cards':     total_rc,
        'avg_attendance':      int(avg_att),
    }


def get_top_scorers(n: int = 10) -> pd.DataFrame:
    """Return top-n players sorted by Goals descending."""
    _, players, _, _ = _load_data()
    cols = ['Name', 'Nation', 'Position', 'Club', 'Goals', 'Assists', 'Minutes', 'Rating']
    return (players[cols]
            .sort_values('Goals', ascending=False)
            .head(n)
            .reset_index(drop=True))


def get_top_assisters(n: int = 10) -> pd.DataFrame:
    """Return top-n players sorted by Assists descending."""
    _, players, _, _ = _load_data()
    cols = ['Name', 'Nation', 'Position', 'Club', 'Goals', 'Assists', 'Minutes', 'Rating']
    return (players[cols]
            .sort_values('Assists', ascending=False)
            .head(n)
            .reset_index(drop=True))


def goals_by_round() -> pd.Series:
    """Return total goals per tournament round, ordered by stage."""
    matches, _, _, _ = _load_data()
    matches = matches.copy()
    matches['total_goals'] = matches['HomeGoals'] + matches['AwayGoals']
    order = ['Group Stage', 'Round of 32', 'Round of 16',
             'Quarter-Final', 'Semi-Final', 'Third Place', 'Final']
    series = matches.groupby('Round')['total_goals'].sum()
    # Reorder by tournament stage
    series = series.reindex([r for r in order if r in series.index])
    return series


def goals_by_confederation() -> pd.Series:
    """Return total goals scored per confederation."""
    matches, _, teams, _ = _load_data()
    conf_map = teams.set_index('Nation')['Confederation'].to_dict()

    rows = []
    for _, m in matches.iterrows():
        ht_conf = conf_map.get(m['HomeTeam'], 'Unknown')
        at_conf = conf_map.get(m['AwayTeam'], 'Unknown')
        rows.append({'Confederation': ht_conf, 'Goals': m['HomeGoals']})
        rows.append({'Confederation': at_conf, 'Goals': m['AwayGoals']})

    return (pd.DataFrame(rows)
              .groupby('Confederation')['Goals']
              .sum()
              .sort_values(ascending=False))


def attendance_summary() -> pd.DataFrame:
    """Return venue-level attendance statistics."""
    matches, _, _, _ = _load_data()
    agg = (matches.groupby(['Venue', 'City', 'Country'])['Attendance']
                  .agg(Matches='count', Total_Attendance='sum', Avg_Attendance='mean', Max_Attendance='max')
                  .reset_index())
    agg['Avg_Attendance'] = agg['Avg_Attendance'].round(0).astype(int)
    agg['Max_Attendance'] = agg['Max_Attendance'].astype(int)
    return agg.sort_values('Avg_Attendance', ascending=False).reset_index(drop=True)


def correlation_matrix() -> pd.DataFrame:
    """Return a correlation matrix of numeric match statistics."""
    matches, _, _, _ = _load_data()
    num_cols = ['HomeGoals', 'AwayGoals', 'HomePossession',
                'HomeShots', 'AwayShots', 'HomeXG', 'AwayXG',
                'Attendance', 'HomeYellowCards', 'AwayYellowCards']
    available = [c for c in num_cols if c in matches.columns]
    return matches[available].corr().round(3)


def host_nation_analysis() -> dict:
    """Compare host-nation match metrics to non-host matches."""
    matches, _, _, _ = _load_data()
    hosts = {'United States', 'Canada', 'Mexico'}

    host_mask = matches['HomeTeam'].isin(hosts) | matches['AwayTeam'].isin(hosts)
    host_matches  = matches[host_mask]
    other_matches = matches[~host_mask]

    def avg_goals(df):
        return round((df['HomeGoals'].sum() + df['AwayGoals'].sum()) / max(len(df), 1), 2)

    return {
        'host_match_count':      len(host_matches),
        'non_host_match_count':  len(other_matches),
        'host_avg_goals':        avg_goals(host_matches),
        'non_host_avg_goals':    avg_goals(other_matches),
        'host_avg_attendance':   int(host_matches['Attendance'].mean()) if len(host_matches) else 0,
        'non_host_avg_attendance': int(other_matches['Attendance'].mean()) if len(other_matches) else 0,
    }


def red_yellow_analysis() -> dict:
    """Return aggregated card statistics for the tournament."""
    matches, _, _, _ = _load_data()
    return {
        'total_yellow_cards': int(matches['HomeYellowCards'].sum() + matches['AwayYellowCards'].sum()),
        'total_red_cards':    int(matches['HomeRedCards'].sum()    + matches['AwayRedCards'].sum()),
        'avg_yellow_per_match': round((matches['HomeYellowCards'] + matches['AwayYellowCards']).mean(), 2),
        'avg_red_per_match':    round((matches['HomeRedCards']    + matches['AwayRedCards']).mean(), 3),
        'most_carded_match': (
            matches.assign(_cards=matches['HomeYellowCards'] + matches['AwayYellowCards'] +
                                  matches['HomeRedCards'] + matches['AwayRedCards'])
                   .sort_values('_cards', ascending=False)
                   .iloc[0][['HomeTeam','AwayTeam','HomeGoals','AwayGoals','Round']]
                   .to_dict()
        ),
    }


def group_performance_summary() -> pd.DataFrame:
    """Return per-group aggregate: total goals, avg goals, total matches."""
    matches, _, teams, _ = _load_data()
    group_map = teams.set_index('Nation')['Group'].to_dict()

    rows = []
    for _, m in matches[matches['Round'] == 'Group Stage'].iterrows():
        grp = group_map.get(m['HomeTeam'], '?')
        rows.append({'Group': grp, 'Goals': m['HomeGoals'] + m['AwayGoals']})

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    return (df.groupby('Group')['Goals']
              .agg(Total_Goals='sum', Avg_Goals='mean', Matches='count')
              .reset_index()
              .sort_values('Total_Goals', ascending=False)
              .reset_index(drop=True))
