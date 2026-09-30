class Agent:
    """Autonomous response agent with local state and resilience metadata."""

    def __init__(self, agent_id, position, capabilities):
        self.agent_id = agent_id
        self.position = position
        self.capabilities = set(capabilities)

        self.current_task = None
        self.path = []

        self.energy = 100.0
        self.communication_available = True
        self.communication_quality = 1.0
        self.active = True

        self.task_path_cost = 0.0
        self.wait_count = 0
        self.replans = 0
        self.completed_tasks = 0

    def can_handle(self, resource_type):
        return resource_type in self.capabilities

    def assign_task(self, incident):
        self.current_task = incident
        self.task_path_cost = 0.0
        self.wait_count = 0

    def set_path(self, path):
        self.path = list(path)

    def move_to_next_position(self):
        if not self.active:
            return

        if len(self.path) > 1:
            self.path.pop(0)
            previous_position = self.position
            self.position = self.path[0]

            if self.position != previous_position:
                self.task_path_cost += 1.0

    def fail(self):
        self.active = False

    def wait(self):
        if self.active:
            self.wait_count += 1

    def lose_communication(self):
        self.communication_available = False
        self.communication_quality = 0.0

    def restore_communication(self):
        self.communication_available = True
        self.communication_quality = 1.0
