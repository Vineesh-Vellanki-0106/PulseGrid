class SimulationMetrics:
    def __init__(self):
        self.completed_tasks = 0
        self.total_path_cost = 0.0
        self.collisions = 0
        self.deadlocks = 0
        self.energy_consumed = 0.0
        self.replans = 0
        self.decision_latencies = []

    def record_task_completion(self, path_length):
        self.completed_tasks += 1
        self.total_path_cost += path_length

    def record_collision(self):
        self.collisions += 1

    def record_deadlock(self):
        self.deadlocks += 1

    def record_replan(self):
        self.replans += 1

    def record_energy(self, amount):
        self.energy_consumed += amount

    def record_latency(self, latency_ms):
        self.decision_latencies.append(latency_ms)

    def average_latency(self):
        if not self.decision_latencies:
            return 0.0

        return (
            sum(self.decision_latencies)
            / len(self.decision_latencies)
        )

    def fitness_score(self):
        latency = self.average_latency()

        score = (
            self.completed_tasks * 100
            - self.total_path_cost
            - self.collisions * 100
            - self.deadlocks * 150
            - self.energy_consumed * 0.1
            - self.replans * 2
            - latency
        )

        return round(score, 2)

    def summary(self):
        return {
            "completed_tasks": self.completed_tasks,
            "total_path_cost": round(self.total_path_cost, 2),
            "collisions": self.collisions,
            "deadlocks": self.deadlocks,
            "energy_consumed": round(self.energy_consumed, 2),
            "replans": self.replans,
            "average_latency_ms": round(
                self.average_latency(), 3
            ),
            "fitness": self.fitness_score()
        }