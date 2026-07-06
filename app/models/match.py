class Match:
    """
    Model representing a football match.
    """
    def __init__(self, match_id, home_team, away_team, date, venue, 
                 home_goals, away_goals, home_possession, away_possession, 
                 home_shots, away_shots, home_shots_on_target, away_shots_on_target, 
                 home_corners, away_corners, home_yellow_cards, away_yellow_cards, 
                 home_red_cards, away_red_cards, winner):
        self.match_id = int(match_id)
        self.home_team = str(home_team).strip()
        self.away_team = str(away_team).strip()
        self.date = str(date).strip()
        self.venue = str(venue).strip()
        self.home_goals = int(home_goals)
        self.away_goals = int(away_goals)
        self.home_possession = int(home_possession)
        self.away_possession = int(away_possession)
        self.home_shots = int(home_shots)
        self.away_shots = int(away_shots)
        self.home_shots_on_target = int(home_shots_on_target)
        self.away_shots_on_target = int(away_shots_on_target)
        self.home_corners = int(home_corners)
        self.away_corners = int(away_corners)
        self.home_yellow_cards = int(home_yellow_cards)
        self.away_yellow_cards = int(away_yellow_cards)
        self.home_red_cards = int(home_red_cards)
        self.away_red_cards = int(away_red_cards)
        self.winner = str(winner).strip()

    @classmethod
    def from_dict(cls, data):
        """
        Create a Match instance from a dictionary.
        """
        return cls(
            match_id=data.get('MatchID'),
            home_team=data.get('HomeTeam', ''),
            away_team=data.get('AwayTeam', ''),
            date=data.get('Date', ''),
            venue=data.get('Venue', ''),
            home_goals=data.get('HomeGoals', 0),
            away_goals=data.get('AwayGoals', 0),
            home_possession=data.get('HomePossession', 0),
            away_possession=data.get('AwayPossession', 0),
            home_shots=data.get('HomeShots', 0),
            away_shots=data.get('AwayShots', 0),
            home_shots_on_target=data.get('HomeShotsOnTarget', 0),
            away_shots_on_target=data.get('AwayShotsOnTarget', 0),
            home_corners=data.get('HomeCorners', 0),
            away_corners=data.get('AwayCorners', 0),
            home_yellow_cards=data.get('HomeYellowCards', 0),
            away_yellow_cards=data.get('AwayYellowCards', 0),
            home_red_cards=data.get('HomeRedCards', 0),
            away_red_cards=data.get('AwayRedCards', 0),
            winner=data.get('Winner', '')
        )

    def to_dict(self):
        """
        Convert Match instance to a dictionary.
        """
        return {
            'match_id': self.match_id,
            'home_team': self.home_team,
            'away_team': self.away_team,
            'date': self.date,
            'venue': self.venue,
            'home_goals': self.home_goals,
            'away_goals': self.away_goals,
            'home_possession': self.home_possession,
            'away_possession': self.away_possession,
            'home_shots': self.home_shots,
            'away_shots': self.away_shots,
            'home_shots_on_target': self.home_shots_on_target,
            'away_shots_on_target': self.away_shots_on_target,
            'home_corners': self.home_corners,
            'away_corners': self.away_corners,
            'home_yellow_cards': self.home_yellow_cards,
            'away_yellow_cards': self.away_yellow_cards,
            'home_red_cards': self.home_red_cards,
            'away_red_cards': self.away_red_cards,
            'winner': self.winner,
            'total_goals': self.home_goals + self.away_goals,
            'is_draw': self.home_goals == self.away_goals
        }

    def __repr__(self):
        return f"<Match {self.home_team} vs {self.away_team} on {self.date}>"
