import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from app.services.loader import load_matches
from app.services.statistics import get_team_stats

# Cache the model so we don't retrain it on every request
_model = None
_label_encoder = None

def prepare_training_data():
    """
    Prepare the dataset for training the ML model.
    Features: HomeTeamAvgScored, HomeTeamAvgConceded, AwayTeamAvgScored, AwayTeamAvgConceded
    Target: 0 for Away Win, 1 for Draw, 2 for Home Win
    """
    matches_df = load_matches(processed=True)
    
    features = []
    targets = []
    
    # Simple encoding for targets
    target_map = {'Away Win': 0, 'Draw': 1, 'Home Win': 2}
    
    # We will build features using historical team stats
    # For a production app, these stats should be "point-in-time" prior to the match.
    # For this dashboard, we will use overall season stats as proxy features.
    
    # Pre-fetch stats to avoid loading them repeatedly
    teams = pd.concat([matches_df['HomeTeam'], matches_df['AwayTeam']]).unique()
    team_stats_cache = {team: get_team_stats(team) for team in teams}
    
    for idx, match in matches_df.iterrows():
        home_team = match['HomeTeam']
        away_team = match['AwayTeam']
        winner = match['Winner']
        
        home_stats = team_stats_cache.get(home_team, {})
        away_stats = team_stats_cache.get(away_team, {})
        
        # Features
        h_scored = home_stats.get('avg_goals_scored', 0)
        h_conceded = home_stats.get('avg_goals_conceded', 0)
        a_scored = away_stats.get('avg_goals_scored', 0)
        a_conceded = away_stats.get('avg_goals_conceded', 0)
        
        features.append([h_scored, h_conceded, a_scored, a_conceded])
        
        # Target
        if winner == home_team:
            targets.append(2)
        elif winner == away_team:
            targets.append(0)
        else:
            targets.append(1)
            
    return pd.DataFrame(features, columns=['HomeScored', 'HomeConceded', 'AwayScored', 'AwayConceded']), pd.Series(targets)

def train_model():
    """
    Train the RandomForest model.
    """
    global _model
    
    X, y = prepare_training_data()
    
    if len(X) < 10:
        # Not enough data
        return False
        
    _model = RandomForestClassifier(n_estimators=100, random_state=42)
    _model.fit(X, y)
    
    return True

def predict_match(home_team, away_team):
    """
    Predict the outcome of a match between home_team and away_team.
    """
    global _model
    
    if _model is None:
        success = train_model()
        if not success:
            return None
            
    home_stats = get_team_stats(home_team)
    away_stats = get_team_stats(away_team)
    
    h_scored = home_stats.get('avg_goals_scored', 0)
    h_conceded = home_stats.get('avg_goals_conceded', 0)
    a_scored = away_stats.get('avg_goals_scored', 0)
    a_conceded = away_stats.get('avg_goals_conceded', 0)
    
    features = pd.DataFrame([[h_scored, h_conceded, a_scored, a_conceded]], 
                            columns=['HomeScored', 'HomeConceded', 'AwayScored', 'AwayConceded'])
                            
    probabilities = _model.predict_proba(features)[0]
    
    # scikit-learn predict_proba orders by classes: 0 (Away), 1 (Draw), 2 (Home)
    away_win_prob = round(probabilities[0] * 100, 2)
    draw_prob = round(probabilities[1] * 100, 2)
    home_win_prob = round(probabilities[2] * 100, 2)
    
    prediction = "Home Win"
    if away_win_prob > home_win_prob and away_win_prob > draw_prob:
        prediction = "Away Win"
    elif draw_prob > home_win_prob and draw_prob > away_win_prob:
        prediction = "Draw"
        
    return {
        'home_team': home_team,
        'away_team': away_team,
        'prediction': prediction,
        'probabilities': {
            'home_win': home_win_prob,
            'draw': draw_prob,
            'away_win': away_win_prob
        }
    }
