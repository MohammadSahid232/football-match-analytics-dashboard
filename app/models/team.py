class Team:
    """
    Model representing a football club.
    """
    def __init__(self, team_id, name, founded, city, stadium, capacity, manager, mascot):
        self.team_id = int(team_id)
        self.name = str(name).strip()
        self.founded = int(founded)
        self.city = str(city).strip()
        self.stadium = str(stadium).strip()
        self.capacity = int(capacity)
        self.manager = str(manager).strip()
        self.mascot = str(mascot).strip()

    @classmethod
    def from_dict(cls, data):
        """
        Create a Team instance from a dictionary.
        """
        return cls(
            team_id=data.get('TeamID'),
            name=data.get('Name'),
            founded=data.get('Founded', 1900),
            city=data.get('City', ''),
            stadium=data.get('Stadium', ''),
            capacity=data.get('Capacity', 0),
            manager=data.get('Manager', ''),
            mascot=data.get('Mascot', '')
        )

    def to_dict(self):
        """
        Convert Team instance to a dictionary.
        """
        return {
            'team_id': self.team_id,
            'name': self.name,
            'founded': self.founded,
            'city': self.city,
            'stadium': self.stadium,
            'capacity': self.capacity,
            'manager': self.manager,
            'mascot': self.mascot
        }

    def __repr__(self):
        return f"<Team {self.name}>"
