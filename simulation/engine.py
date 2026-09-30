import time
from evaluation.metrics import SimulationMetrics
from agents.task_allocator import TaskAllocator
from planning.astar import AStarPlanner
from planning.collision_avoidance import CollisionDetector
from planning.astar import AStarPlanner
from planning.collision_avoidance import CollisionDetector
from agents.task_allocator import TaskAllocator 

class SimulationEngine:
    def __init__(self, environment):
        self.environment = environment
        self.planner = AStarPlanner(environment)
        self.collision_detector = CollisionDetector()
        self.task_allocator = TaskAllocator()
        self.agents = []
        self.tick = 0
        self.running = False
        self.metrics = SimulationMetrics()

    def add_agent(self, agent):
        self.agents.append(agent)


    def assign_path(self, agent, destination):
        if not agent.active:
             return False

        path = self.planner.find_path(
            agent.position,
            destination
        )

        if not path:
            return False

        agent.set_path(path)
        return True

    def allocate_incident(self, incident):
        active_agents = [
            agent
            for agent in self.agents
            if agent.active and agent.current_task is None
        ]

        if not active_agents:
            return None

        winner = self.task_allocator.allocate_task(
            active_agents,
            incident
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
                    "agent_id": winner.agent_id
                })

        return assignments


    def replan_if_blocked(self, agent, destination):
        if not agent.active:
            return False

        if not agent.path:
             return self.assign_path(agent, destination)

        for position in agent.path:
            if not self.environment.is_walkable(position):
                result = self.assign_path(
                    agent,
                    destination
                )

                if result:
                    self.metrics.record_replan()

                return result

        return True

    def detect_collisions(self):
        agent_paths = {
        agent.agent_id: agent.path
        for agent in self.agents
        if agent.active and agent.path
        }

        return self.collision_detector.detect_vertex_conflicts(
        agent_paths
        )

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def advance_tick(self):
        if not self.running:
            return

        start_time = time.perf_counter()

        self.tick += 1

        waiting_agents = self.resolve_collisions()

        for agent in self.agents:
            if not agent.active:
                continue

            # Complete task if agent has reached incident
            if (
                agent.current_task is not None
                and agent.position == agent.current_task.position
            ):
                incident = agent.current_task

                incident.complete()

                self.metrics.record_task_completion(
                    agent.task_path_cost
                )

                agent.current_task = None
                agent.path = []
                agent.task_path_cost = 0.0

                continue

            # Replan if dynamic obstacle blocked current route
            if agent.current_task is not None:
                self.replan_if_blocked(
                    agent,
                    agent.current_task.position
                )

            if agent.agent_id in waiting_agents:
                agent.wait()
            else:
                previous_position = agent.position

                agent.move_to_next_position()

                if agent.position != previous_position:
                    agent.energy = max(0.0, agent.energy - 1.0)
                    self.metrics.record_energy(1.0)

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        self.metrics.record_latency(latency_ms)

    def resolve_collisions(self):
        agent_paths = {
            agent.agent_id: agent.path
            for agent in self.agents
            if agent.active and agent.path
        }

        resolutions = self.collision_detector.resolve_vertex_conflicts(
            agent_paths
        )

        waiting_agents = {
            resolution["waiting_agent"]
            for resolution in resolutions
            if resolution["tick"] == 1
        }

        return waiting_agents

    def reassign_failed_tasks(self, incidents):
        reassigned = []

        results = self.task_allocator.reassign_failed_tasks(
            self.agents,
            incidents
        )

        for assignment in results:
            for agent in self.agents:
                if agent.agent_id == assignment["agent_id"]:
                    incident = next(
                        (
                            i for i in incidents
                            if i.incident_id == assignment["incident_id"]
                        ),
                        None
                    )

                    if incident is not None:
                        self.assign_path(
                            agent,
                            incident.position
                        )

                        reassigned.append({
                            "agent_id": agent.agent_id,
                            "incident_id": incident.incident_id
                        })

        return reassigned