"""
fifa2026_visualization.py
Generates 8 publication-quality charts for the FIFA 2026 dataset.

Charts produced (saved to static/images/fifa2026/):
  1. top_scorers_bar.png       - Top 10 goal scorers (horizontal bar)
  2. goals_by_round.png        - Goals per tournament round (bar)
  3. goals_distribution.png    - Goals per match (histogram + KDE)
  4. team_win_rate.png         - Win rate of top 20 teams (bar)
  5. possession_vs_goals.png   - Possession % vs Goals (scatter)
  6. attendance_by_venue.png   - Avg attendance per host city (bar)
  7. confederation_goals.png   - Goals by confederation (pie)
  8. correlation_heatmap.png   - Numeric match stat heatmap (Seaborn)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np

from app.services.fifa2026_loader import (
    load_matches, load_players, load_teams
)
from app.services.fifa2026_eda import (
    get_top_scorers, goals_by_round, goals_by_confederation,
    attendance_summary, correlation_matrix
)

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHART_DIR = os.path.join(BASE_DIR, 'static', 'images', 'fifa2026')
os.makedirs(CHART_DIR, exist_ok=True)

# ── Design tokens ───────────────────────────────────────
DARK_BG   = '#0d1117'
CARD_BG   = '#161b22'
ACCENT    = '#238636'
ACCENT2   = '#1f6feb'
TEXT      = '#e6edf3'
GOLD      = '#e3b341'
RED_CLR   = '#f85149'
PALETTE   = ['#238636', '#1f6feb', '#e3b341', '#f85149',
             '#8b949e', '#bc8cff', '#79c0ff', '#56d364',
             '#d29922', '#ff7b72']

plt.rcParams.update({
    'figure.facecolor':  DARK_BG,
    'axes.facecolor':    CARD_BG,
    'axes.edgecolor':    '#30363d',
    'axes.labelcolor':   TEXT,
    'axes.titlecolor':   TEXT,
    'xtick.color':       TEXT,
    'ytick.color':       TEXT,
    'text.color':        TEXT,
    'grid.color':        '#21262d',
    'grid.linewidth':    0.6,
    'font.family':       'DejaVu Sans',
})


def _save(name: str) -> None:
    path = os.path.join(CHART_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print(f"  [chart] Saved {name}")


# ─────────────────────────────────────────────────────────
# 1. Top Scorers Horizontal Bar
# ─────────────────────────────────────────────────────────
def plot_top_scorers():
    df = get_top_scorers(10)
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=DARK_BG)
    colors = [GOLD if i == 0 else ACCENT for i in range(len(df))]
    bars = ax.barh(df['Name'][::-1], df['Goals'][::-1], color=colors[::-1],
                   edgecolor='#30363d', height=0.65)
    for bar, g in zip(bars, df['Goals'][::-1]):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                str(int(g)), va='center', fontsize=10, color=GOLD, fontweight='bold')
    ax.set_xlabel('Goals Scored', fontsize=11)
    ax.set_title('FIFA 2026 World Cup — Top 10 Goal Scorers', fontsize=14,
                 fontweight='bold', pad=14, color=GOLD)
    ax.grid(axis='x', alpha=0.4)
    ax.set_xlim(0, df['Goals'].max() + 1.5)
    _save('top_scorers_bar.png')


# ─────────────────────────────────────────────────────────
# 2. Goals by Round Bar
# ─────────────────────────────────────────────────────────
def plot_goals_by_round():
    series = goals_by_round()
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=DARK_BG)
    bars = ax.bar(series.index, series.values, color=PALETTE[:len(series)],
                  edgecolor='#30363d', width=0.6)
    for bar, val in zip(bars, series.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                str(int(val)), ha='center', fontsize=10, color=TEXT, fontweight='bold')
    ax.set_xlabel('Tournament Round', fontsize=11)
    ax.set_ylabel('Total Goals', fontsize=11)
    ax.set_title('Total Goals per Tournament Round — FIFA 2026', fontsize=14,
                 fontweight='bold', pad=14, color=GOLD)
    plt.xticks(rotation=30, ha='right')
    ax.grid(axis='y', alpha=0.4)
    _save('goals_by_round.png')


# ─────────────────────────────────────────────────────────
# 3. Goals Distribution (Histogram + KDE)
# ─────────────────────────────────────────────────────────
def plot_goals_distribution():
    try:
        matches = load_matches(processed=True)
    except FileNotFoundError:
        matches = load_matches(processed=False)

    total_goals = matches['HomeGoals'] + matches['AwayGoals']
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=DARK_BG)
    ax.hist(total_goals, bins=range(0, int(total_goals.max()) + 2),
            color=ACCENT2, edgecolor=DARK_BG, alpha=0.75, density=True, label='Histogram')

    # KDE overlay
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(total_goals)
    x   = np.linspace(0, total_goals.max() + 1, 200)
    ax.plot(x, kde(x), color=GOLD, linewidth=2.5, label='KDE')

    ax.axvline(total_goals.mean(), color=RED_CLR, linestyle='--', linewidth=1.8,
               label=f'Mean = {total_goals.mean():.2f}')
    ax.set_xlabel('Goals per Match', fontsize=11)
    ax.set_ylabel('Density', fontsize=11)
    ax.set_title('Goals per Match — Distribution (FIFA 2026)', fontsize=14,
                 fontweight='bold', pad=14, color=GOLD)
    ax.legend(facecolor=CARD_BG)
    ax.grid(alpha=0.4)
    _save('goals_distribution.png')


# ─────────────────────────────────────────────────────────
# 4. Team Win Rate Bar (top 20)
# ─────────────────────────────────────────────────────────
def plot_team_win_rate():
    try:
        matches = load_matches(processed=True)
    except FileNotFoundError:
        matches = load_matches(processed=False)
    try:
        teams_df = load_teams(processed=True)
    except FileNotFoundError:
        teams_df = load_teams(processed=False)

    nations = teams_df['Nation'].tolist()
    rows = []
    for n in nations:
        home = matches[matches['HomeTeam'] == n]
        away = matches[matches['AwayTeam'] == n]
        played = len(home) + len(away)
        if played == 0:
            continue
        wins = (home['Winner'] == n).sum() + (away['Winner'] == n).sum()
        rows.append({'Nation': n, 'WinRate': round(wins / played * 100, 1), 'Played': played})

    df = pd.DataFrame(rows).sort_values('WinRate', ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(12, 5), facecolor=DARK_BG)
    bar_colors = [GOLD if i == 0 else (ACCENT if i < 3 else ACCENT2) for i in range(len(df))]
    ax.bar(df['Nation'], df['WinRate'], color=bar_colors, edgecolor='#30363d', width=0.7)
    ax.set_xlabel('Nation', fontsize=11)
    ax.set_ylabel('Win Rate (%)', fontsize=11)
    ax.set_title('Team Win Rate — Top 20 Nations (FIFA 2026)', fontsize=14,
                 fontweight='bold', pad=14, color=GOLD)
    plt.xticks(rotation=40, ha='right', fontsize=8)
    ax.grid(axis='y', alpha=0.4)
    _save('team_win_rate.png')


# ─────────────────────────────────────────────────────────
# 5. Possession vs Goals Scatter
# ─────────────────────────────────────────────────────────
def plot_possession_vs_goals():
    try:
        matches = load_matches(processed=True)
    except FileNotFoundError:
        matches = load_matches(processed=False)

    fig, ax = plt.subplots(figsize=(9, 6), facecolor=DARK_BG)
    # Combine home and away perspectives
    home = matches[['HomePossession', 'HomeGoals']].rename(
        columns={'HomePossession': 'Possession', 'HomeGoals': 'Goals'})
    away = matches[['AwayPossession', 'AwayGoals']].rename(
        columns={'AwayPossession': 'Possession', 'AwayGoals': 'Goals'})
    combined = pd.concat([home, away], ignore_index=True)

    scatter = ax.scatter(combined['Possession'], combined['Goals'],
                         c=combined['Goals'], cmap='RdYlGn',
                         alpha=0.65, edgecolors='#30363d', linewidths=0.5, s=60)
    plt.colorbar(scatter, ax=ax, label='Goals Scored')

    # Trend line
    z = np.polyfit(combined['Possession'], combined['Goals'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(combined['Possession'].min(), combined['Possession'].max(), 100)
    ax.plot(x_line, p(x_line), color=GOLD, linewidth=2, linestyle='--', label='Trend')

    ax.set_xlabel('Ball Possession (%)', fontsize=11)
    ax.set_ylabel('Goals Scored', fontsize=11)
    ax.set_title('Possession vs Goals Scored — FIFA 2026', fontsize=14,
                 fontweight='bold', pad=14, color=GOLD)
    ax.legend(facecolor=CARD_BG)
    ax.grid(alpha=0.4)
    _save('possession_vs_goals.png')


# ─────────────────────────────────────────────────────────
# 6. Attendance by Venue
# ─────────────────────────────────────────────────────────
def plot_attendance_by_venue():
    att_df = attendance_summary()
    fig, ax = plt.subplots(figsize=(14, 6), facecolor=DARK_BG)
    colors = [GOLD if i == 0 else ACCENT for i in range(len(att_df))]
    ax.bar(att_df['Venue'], att_df['Avg_Attendance'], color=colors,
           edgecolor='#30363d', width=0.7)
    ax.set_xlabel('Venue', fontsize=11)
    ax.set_ylabel('Avg Attendance', fontsize=11)
    ax.set_title('Average Attendance per Venue — FIFA 2026', fontsize=14,
                 fontweight='bold', pad=14, color=GOLD)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    ax.grid(axis='y', alpha=0.4)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    _save('attendance_by_venue.png')


# ─────────────────────────────────────────────────────────
# 7. Goals by Confederation Pie Chart
# ─────────────────────────────────────────────────────────
def plot_confederation_goals():
    series = goals_by_confederation()
    colors = PALETTE[:len(series)]
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=DARK_BG)
    wedges, texts, autotexts = ax.pie(
        series.values, labels=series.index,
        autopct='%1.1f%%', colors=colors,
        startangle=140, pctdistance=0.82,
        wedgeprops={'edgecolor': DARK_BG, 'linewidth': 2}
    )
    for t in texts:
        t.set_color(TEXT); t.set_fontsize(10)
    for at in autotexts:
        at.set_color(DARK_BG); at.set_fontsize(9); at.set_fontweight('bold')
    ax.set_title('Goals by Confederation — FIFA 2026', fontsize=14,
                 fontweight='bold', pad=18, color=GOLD)
    _save('confederation_goals.png')


# ─────────────────────────────────────────────────────────
# 8. Correlation Heatmap
# ─────────────────────────────────────────────────────────
def plot_correlation_heatmap():
    corr = correlation_matrix()
    fig, ax = plt.subplots(figsize=(10, 8), facecolor=DARK_BG)
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn',
                linewidths=0.5, linecolor=DARK_BG,
                ax=ax, center=0,
                annot_kws={'size': 8, 'color': TEXT},
                cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Heatmap — FIFA 2026 Match Statistics',
                 fontsize=13, fontweight='bold', pad=14, color=GOLD)
    plt.xticks(rotation=35, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    _save('correlation_heatmap.png')


# ─────────────────────────────────────────────────────────
# GENERATE ALL
# ─────────────────────────────────────────────────────────
def generate_all_charts():
    """Generate all 8 FIFA 2026 visualization charts."""
    print("\n[Visualizations] Generating FIFA 2026 charts ...")
    plot_top_scorers()
    plot_goals_by_round()
    plot_goals_distribution()
    plot_team_win_rate()
    plot_possession_vs_goals()
    plot_attendance_by_venue()
    plot_confederation_goals()
    plot_correlation_heatmap()
    print(f"[Visualizations] All 8 charts saved to: {CHART_DIR}\n")


if __name__ == '__main__':
    generate_all_charts()
