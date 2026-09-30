from collections import defaultdict


class GridEnvironment:
    """Grid world with dynamic obstacles and a lightweight congestion field."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = set()
        self.incidents = {}
        self.congestion = defaultdict(float)

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, position):
        return (
            self.is_valid_position(position)
            and position not in self.obstacles
        )

    def add_obstacle(self, position):
        if self.is_valid_position(position):
            self.obstacles.add(position)

    def remove_obstacle(self, position):
        self.obstacles.discard(position)

    def add_incident(self, incident):
        if self.is_valid_position(incident.position):
            self.incidents[incident.incident_id] = incident

    def add_congestion(self, position, amount=1.0):
        if self.is_valid_position(position):
            self.congestion[position] += max(0.0, amount)

    def get_congestion(self, position):
        return float(self.congestion.get(position, 0.0))

    def decay_congestion(self, decay=0.90):
        """Forget old traffic gradually, emulating local stigmergic memory."""
        for position in list(self.congestion):
            self.congestion[position] *= decay
            if self.congestion[position] < 0.05:
                del self.congestion[position]
