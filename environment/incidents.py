class Incident:
    def __init__(self, incident_id, position, severity, resource_type):
        self.incident_id = incident_id
        self.position = position
        self.severity = severity
        self.resource_type = resource_type
        self.completed = False

    def complete(self):
        self.completed = True