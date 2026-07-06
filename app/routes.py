import os
from flask import Blueprint, render_template, request, jsonify
from app.services.loader import load_teams, load_players, load_matches, load_standings
from app.services.analytics import get_dashboard_metrics
from app.services.statistics import get_all_teams_stats, get_top_scorers, get_top_assists, get_top_players
from app.services.team_analysis import compare_teams, team_performance_trend
from app.services.player_analysis import compare_players, get_player_efficiency
from app.services.match_analysis import get_match_distribution_by_venue
from app.services.predictions import predict_match
from app.services.visualization import generate_all_charts

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    metrics = get_dashboard_metrics()
    return render_template('index.html', metrics=metrics)

@main_bp.route('/teams')
def teams():
    teams_df = load_teams(processed=True)
    teams_list = teams_df.to_dict(orient='records')
    return render_template('teams.html', teams=teams_list)

@main_bp.route('/players')
def players():
    players_df = load_players(processed=True)
    players_list = players_df.to_dict(orient='records')
    return render_template('players.html', players=players_list)

@main_bp.route('/matches')
def matches():
    matches_df = load_matches(processed=True)
    matches_list = matches_df.to_dict(orient='records')
    return render_template('matches.html', matches=matches_list)

@main_bp.route('/statistics')
def statistics():
    standings_df = load_standings(processed=True)
    standings = standings_df.to_dict(orient='records')
    top_scorers = get_top_scorers(limit=10)
    top_assists = get_top_assists(limit=10)
    
    return render_template('statistics.html', 
                           standings=standings, 
                           top_scorers=top_scorers, 
                           top_assists=top_assists)

@main_bp.route('/analytics')
def analytics():
    venue_stats = get_match_distribution_by_venue()
    teams_stats = get_all_teams_stats().to_dict(orient='records')
    return render_template('analytics.html', venue_stats=venue_stats, teams_stats=teams_stats)

@main_bp.route('/visualization')
def visualization():
    # Ensure charts exist before rendering the template
    charts = generate_all_charts()
    return render_template('visualization.html', charts=charts)

@main_bp.route('/prediction', methods=['GET', 'POST'])
def prediction():
    teams_df = load_teams(processed=True)
    teams = teams_df['Name'].tolist()
    
    prediction_result = None
    if request.method == 'POST':
        home_team = request.form.get('home_team')
        away_team = request.form.get('away_team')
        if home_team and away_team and home_team != away_team:
            prediction_result = predict_match(home_team, away_team)
            
    return render_template('prediction.html', teams=teams, prediction_result=prediction_result)

@main_bp.route('/about')
def about():
    return render_template('about.html')
