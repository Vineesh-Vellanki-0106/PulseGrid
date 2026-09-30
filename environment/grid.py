class GridEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = set()
        self.incidents = {}

    def is_valid_position(self, position):
        x, y = position

        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

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