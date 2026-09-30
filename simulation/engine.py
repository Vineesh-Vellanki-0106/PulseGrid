import time

from agents.task_allocator import TaskAllocator
from evaluation.metrics import SimulationMetrics
from planning.astar import AStarPlanner
from planning.collision_avoidance import CollisionDetector


class SimulationEngine:
    """Decentralized execution engine with adaptive allocation and replanning."""

    def __init__(self, environment):
        self.environment = environment
        self.planner = AStarPlanner(environment)
        self.collision_detector = CollisionDetector()
        self.task_allocator = TaskAllocator(environment, self.planner)
        self.agents = []
        self.tick = 0
        self.running = False
        self.metrics = SimulationMetrics()
        self.event_log = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def _build_reservations(self, exclude_agent=None):
        reservations = {}
        edge_reservations = {}

        for agent in self.agents:
            if not agent.active or not agent.path:
                continue
            if exclude_agent and agent.agent_id == exclude_agent.agent_id:
                continue

            for tick, position in enumerate(agent.path):
                reservations.setdefault(tick, set()).add(position)

            for tick in range(1, len(agent.path)):
                edge_reservations.setdefault(tick, set()).add(
                    (agent.path[tick - 1], agent.path[tick])
                )
        return reservations, edge_reservations

    def assign_path(self, agent, destination):
        if not agent.active:
            return False

        reservations, edge_reservations = self._build_reservations(agent)
        path = self.planner.find_path(
            agent.position,
            destination,
            reservations=reservations,
            edge_reservations=edge_reservations,
            congestion_weight=0.8,
        )

        if not path:
            # Fallback: ignore reservations when the environment is
            # temporarily over-constrained; collision resolution still
            # provides deterministic local coordination.
            path = self.planner.find_path(
                agent.position,
                destination,
                congestion_weight=0.5,
            )

        if not path:
            return False

        agent.set_path(path)
        return True

    def allocate_incident(self, incident):
        active_agents = [
            agent for agent in self.agents
            if agent.active and agent.current_task is None
        ]
        if not active_agents:
            return None

        winner = self.task_allocator.allocate_task(
            active_agents, incident
        )
        if winner is None:
            return None

        if not self.assign_path(winner, incident.position):
            winner.current_task = None
            return None

        return winner

    def allocate_all_incidents(self, incidents):
        assignments = []
        for incident in incidents:
            if incident.completed:
                continue
            winner = self.allocate_incident(incident)
            if winner is not None:
                assignments.append({
                    "incident_id": incident.incident_id,
                    "agent_id": winner.agent_id,
                })
        return assignments

    def replan_if_blocked(self, agent, destination):
        if not agent.active:
            return False

        if not agent.path:
            return self.assign_path(agent, destination)

        blocked = any(
            not self.environment.is_walkable(position)
            for position in agent.path
        )

        if blocked:
            result = self.assign_path(agent, destination)
            if result:
                agent.replans += 1
                self.metrics.record_replan()
                self.event_log.append({
                    "tick": self.tick,
                    "type": "replan",
                    "agent": agent.agent_id,
                })
            return result

        return True

    def detect_collisions(self):
        agent_paths = {
            agent.agent_id: agent.path
            for agent in self.agents
            if agent.active and agent.path
        }
        return self.collision_detector.detect_conflicts(agent_paths)

    def resolve_collisions(self):
        agent_paths = {
            agent.agent_id: agent.path
            for agent in self.agents
            if agent.active and agent.path
        }

        conflicts = self.collision_detector.detect_conflicts(agent_paths)
        self.metrics.record_conflicts(conflicts)
        resolutions = self.collision_detector.resolve_conflicts(agent_paths)

        # Only conflicts on the immediate next transition affect this tick.
        waiting_agents = set()
        for resolution in resolutions:
            if resolution["tick"] == 1:
                waiting_agents.add(resolution["waiting_agent"])

        return waiting_agents

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def advance_tick(self):
        if not self.running:
            return

        start_time = time.perf_counter()
        self.tick += 1

        self.environment.decay_congestion()
        waiting_agents = self.resolve_collisions()

        for agent in self.agents:
            if not agent.active:
                continue

            if (
                agent.current_task is not None
                and agent.position == agent.current_task.position
            ):
                incident = agent.current_task
                incident.complete()
                agent.completed_tasks += 1
                self.metrics.record_task_completion(
                    agent.task_path_cost
                )
                agent.current_task = None
                agent.path = []
                agent.task_path_cost = 0.0
                continue

            if agent.current_task is not None:
                self.replan_if_blocked(
                    agent, agent.current_task.position
                )

            if agent.agent_id in waiting_agents:
                agent.wait()
                if agent.wait_count == 6:
                    self.metrics.record_deadlock()
            else:
                previous_position = agent.position
                agent.move_to_next_position()

                if agent.position != previous_position:
                    self.environment.add_congestion(
                        agent.position, 1.0
                    )
                    agent.energy = max(0.0, agent.energy - 1.0)
                    self.metrics.record_energy(1.0)

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000.0
        self.metrics.record_latency(latency_ms)

    def reassign_failed_tasks(self, incidents):
        reassigned = self.task_allocator.reassign_failed_tasks(
            self.agents, incidents
        )

        results = []
        for assignment in reassigned:
            incident = next(
                (
                    item for item in incidents
                    if item.incident_id == assignment["incident_id"]
                ),
                None,
            )
            agent = next(
                (
                    item for item in self.agents
                    if item.agent_id == assignment["agent_id"]
                ),
                None,
            )

            if incident is not None and agent is not None:
                if self.assign_path(agent, incident.position):
                    results.append({
                        "agent_id": agent.agent_id,
                        "incident_id": incident.incident_id,
                    })
                    self.event_log.append({
                        "tick": self.tick,
                        "type": "reassignment",
                        "agent": agent.agent_id,
                        "incident": incident.incident_id,
                    })

        return results
