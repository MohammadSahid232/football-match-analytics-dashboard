from app.services.statistics import get_league_summary, get_top_scorers, get_top_assists
from app.services.loader import load_standings
from app.services.match_analysis import get_recent_matches

def get_dashboard_metrics():
    """
    Compile all metrics needed for the main dashboard view.
    """
    summary = get_league_summary()
    
    # Get top 5 standings
    standings_df = load_standings(processed=True)
    top_standings = standings_df.head(5).to_dict(orient='records')
    
    top_scorers = get_top_scorers(limit=5)
    top_assists = get_top_assists(limit=5)
    recent_matches = get_recent_matches(limit=5)
    
    return {
        'summary': summary,
        'top_standings': top_standings,
        'top_scorers': top_scorers,
        'top_assists': top_assists,
        'recent_matches': recent_matches
    }
