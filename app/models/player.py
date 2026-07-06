class Player:
    """
    Model representing a football player.
    """
    def __init__(self, player_id, name, age, position, club, nationality, 
                 goals, assists, yellow_cards, red_cards, matches_played, 
                 minutes_played, rating):
        self.player_id = int(player_id)
        self.name = str(name).strip()
        self.age = int(age)
        self.position = str(position).strip()
        self.club = str(club).strip()
        self.nationality = str(nationality).strip()
        self.goals = int(goals)
        self.assists = int(assists)
        self.yellow_cards = int(yellow_cards)
        self.red_cards = int(red_cards)
        self.matches_played = int(matches_played)
        self.minutes_played = int(minutes_played)
        self.rating = float(rating)

    @classmethod
    def from_dict(cls, data):
        """
        Create a Player instance from a dictionary.
        """
        return cls(
            player_id=data.get('PlayerID'),
            name=data.get('Name'),
            age=data.get('Age', 0),
            position=data.get('Position', ''),
            club=data.get('Club', ''),
            nationality=data.get('Nationality', ''),
            goals=data.get('Goals', 0),
            assists=data.get('Assists', 0),
            yellow_cards=data.get('Yellow Cards', 0),
            red_cards=data.get('Red Cards', 0),
            matches_played=data.get('Matches Played', 0),
            minutes_played=data.get('Minutes Played', 0),
            rating=data.get('Rating', 6.0)
        )

    def to_dict(self):
        """
        Convert Player instance to a dictionary.
        """
        return {
            'player_id': self.player_id,
            'name': self.name,
            'age': self.age,
            'position': self.position,
            'club': self.club,
            'nationality': self.nationality,
            'goals': self.goals,
            'assists': self.assists,
            'yellow_cards': self.yellow_cards,
            'red_cards': self.red_cards,
            'matches_played': self.matches_played,
            'minutes_played': self.minutes_played,
            'rating': self.rating,
            'goal_contribution': self.goals + self.assists,
            'minutes_per_contribution': round(self.minutes_played / (self.goals + self.assists), 1) if (self.goals + self.assists) > 0 else 0.0
        }

    def __repr__(self):
        return f"<Player {self.name} ({self.club})>"
