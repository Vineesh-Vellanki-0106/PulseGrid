class SimulationMetrics:
    def __init__(self):
        self.completed_tasks = 0
        self.total_path_cost = 0.0
        self.collisions = 0
        self.conflicts_detected = 0
        self.conflicts_avoided = 0
        self.edge_conflicts = 0
        self.deadlocks = 0
        self.energy_consumed = 0.0
        self.replans = 0
        self.decision_latencies = []

    def record_task_completion(self, path_length):
        self.completed_tasks += 1
        self.total_path_cost += path_length

    def record_collision(self):
        self.collisions += 1

    def record_conflicts(self, conflicts):
        self.conflicts_detected += len(conflicts)
        self.conflicts_avoided += sum(
            1 for conflict in conflicts
            if conflict.get("type") in {"vertex", "edge"}
        )
        self.edge_conflicts += sum(
            1 for conflict in conflicts
            if conflict.get("type") == "edge"
        )

    def record_deadlock(self):
        self.deadlocks += 1

    def record_replan(self):
        self.replans += 1

    def record_energy(self, amount):
        self.energy_consumed += amount

    def record_latency(self, latency_ms):
        self.decision_latencies.append(float(latency_ms))

    def average_latency(self):
        if not self.decision_latencies:
            return 0.0
        return sum(self.decision_latencies) / len(
            self.decision_latencies
        )

    def percentile_latency(self, percentile):
        if not self.decision_latencies:
            return 0.0
        values = sorted(self.decision_latencies)
        index = (len(values) - 1) * percentile / 100.0
        lower = int(index)
        upper = min(lower + 1, len(values) - 1)
        fraction = index - lower
        return (
            values[lower] * (1.0 - fraction)
            + values[upper] * fraction
        )

    def fitness_score(self):
        latency = self.average_latency()
        return round(
            self.completed_tasks * 100
            - self.total_path_cost
            - self.collisions * 100
            - self.deadlocks * 150
            - self.energy_consumed * 0.1
            - self.replans * 2
            - latency,
            2,
        )

    def summary(self):
        return {
            "completed_tasks": self.completed_tasks,
            "total_path_cost": round(self.total_path_cost, 2),
            "collisions": self.collisions,
            "conflicts_detected": self.conflicts_detected,
            "conflicts_avoided": self.conflicts_avoided,
            "edge_conflicts": self.edge_conflicts,
            "deadlocks": self.deadlocks,
            "energy_consumed": round(self.energy_consumed, 2),
            "replans": self.replans,
            "average_latency_ms": round(
                self.average_latency(), 3
            ),
            "p50_latency_ms": round(
                self.percentile_latency(50), 3
            ),
            "p95_latency_ms": round(
                self.percentile_latency(95), 3
            ),
            "p99_latency_ms": round(
                self.percentile_latency(99), 3
            ),
            "fitness": self.fitness_score(),
        }
