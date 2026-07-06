import pandas as pd
from app.services.loader import load_matches

def get_match_distribution_by_venue():
    """
    Get the number of matches played at each venue and average goals.
    """
    matches_df = load_matches(processed=True)
    
    venue_stats = []
    venues = matches_df['Venue'].unique()
    
    for venue in venues:
        venue_matches = matches_df[matches_df['Venue'] == venue]
        total_matches = len(venue_matches)
        total_goals = venue_matches['HomeGoals'].sum() + venue_matches['AwayGoals'].sum()
        avg_goals = round(total_goals / total_matches, 2) if total_matches > 0 else 0.0
        
        venue_stats.append({
            'venue': venue,
            'total_matches': total_matches,
            'total_goals': int(total_goals),
            'avg_goals': float(avg_goals)
        })
        
    return sorted(venue_stats, key=lambda x: x['total_matches'], reverse=True)

def get_recent_matches(limit=5):
    """
    Get the most recent matches.
    """
    matches_df = load_matches(processed=True)
    recent = matches_df.sort_values(by='Date', ascending=False).head(limit)
    return recent.to_dict(orient='records')
