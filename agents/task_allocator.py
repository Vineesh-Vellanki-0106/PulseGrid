class TaskAllocator:
    """Local auction allocator with an adaptive heuristic.

    When no environment/planner is supplied, the legacy deterministic cost
    remains available for unit tests and simple callers. The simulation engine
    supplies both and uses the adaptive score.
    """

    def __init__(self, environment=None, planner=None):
        self.environment = environment
        self.planner = planner
        self.weights = {
            "distance": 1.0,
            "urgency": 1.0,
            "energy": 0.10,
            "congestion": 0.75,
            "communication": 5.0,
            "risk": 1.5,
        }

    def calculate_cost(self, agent, incident):
        """Backward-compatible baseline cost."""
        if not agent.active or not agent.communication_available:
            return float("inf")
        if not agent.can_handle(incident.resource_type):
            return float("inf")

        distance = (
            abs(agent.position[0] - incident.position[0])
            + abs(agent.position[1] - incident.position[1])
        )
        urgency_penalty = (6 - incident.severity) * 5
        energy_penalty = (100 - agent.energy) * 0.1
        return distance + urgency_penalty + energy_penalty

    def _normalized_distance(self, agent, incident):
        return (
            abs(agent.position[0] - incident.position[0])
            + abs(agent.position[1] - incident.position[1])
        )

    def adaptive_cost(self, agent, incident, assigned_positions=None):
        if not agent.active or not agent.communication_available:
            return float("inf")
        if not agent.can_handle(incident.resource_type):
            return float("inf")

        distance = self._normalized_distance(agent, incident)
        congestion = (
            self.environment.get_congestion(incident.position)
            if self.environment is not None
            else 0.0
        )

        local_load = len(agent.path)
        if assigned_positions and agent.position in assigned_positions:
            local_load += assigned_positions[agent.position]

        # Higher severity means a stronger urgency benefit.
        urgency_bonus = max(0.0, float(incident.severity) / 5.0)
        energy_risk = max(0.0, (50.0 - agent.energy) / 50.0)
        comm_risk = 1.0 - getattr(agent, "communication_quality", 1.0)
        congestion_risk = min(1.0, congestion / 5.0)
        load_risk = min(1.0, local_load / 10.0)

        # Adapt the weights to current swarm stress.
        weights = dict(self.weights)
        if congestion_risk > 0.4:
            weights["congestion"] *= 1.8
            weights["risk"] *= 1.3
        if energy_risk > 0.3:
            weights["energy"] *= 1.8
        if comm_risk > 0.0:
            weights["communication"] *= 2.0

        # Small urgency reduction keeps high-priority incidents attractive.
        return (
            weights["distance"] * distance
            + weights["urgency"] * (6 - incident.severity) * 2.0
            + weights["energy"] * energy_risk * 10.0
            + weights["congestion"] * congestion_risk * 10.0
            + weights["communication"] * comm_risk
            + weights["risk"] * load_risk * 5.0
            - urgency_bonus * 3.0
        )

    def collect_bids(self, agents, incident, assigned_positions=None):
        bids = []
        for agent in agents:
            if self.environment is not None:
                cost = self.adaptive_cost(
                    agent, incident, assigned_positions
                )
            else:
                cost = self.calculate_cost(agent, incident)

            if cost != float("inf"):
                bids.append({
                    "agent_id": agent.agent_id,
                    "cost": round(cost, 6),
                })
        return bids

    def select_winner(self, bids):
        if not bids:
            return None
        return min(
            bids,
            key=lambda bid: (bid["cost"], bid["agent_id"]),
        )

    def allocate_task(self, agents, incident):
        assigned_positions = {}
        bids = self.collect_bids(agents, incident, assigned_positions)
        winner = self.select_winner(bids)
        if winner is None:
            return None

        for agent in agents:
            if agent.agent_id == winner["agent_id"]:
                agent.assign_task(incident)
                return agent
        return None

    def allocate_tasks(self, agents, incidents):
        assignments = []
        assigned_positions = {}

        for incident in incidents:
            if incident.completed:
                continue

            available_agents = [
                agent for agent in agents
                if agent.active and agent.current_task is None
            ]
            if not available_agents:
                break

            bids = self.collect_bids(
                available_agents,
                incident,
                assigned_positions,
            )
            winner = self.select_winner(bids)
            if winner is None:
                continue

            selected = next(
                agent for agent in available_agents
                if agent.agent_id == winner["agent_id"]
            )
            selected.assign_task(incident)
            assigned_positions[selected.position] = (
                assigned_positions.get(selected.position, 0) + 1
            )
            assignments.append({
                "incident_id": incident.incident_id,
                "agent_id": selected.agent_id,
            })

        return assignments

    def reassign_failed_tasks(self, agents, incidents):
        reassigned = []
        for incident in incidents:
            if incident.completed:
                continue

            assigned_agent = next(
                (
                    agent for agent in agents
                    if agent.current_task == incident
                ),
                None,
            )

            if assigned_agent is not None and assigned_agent.active:
                continue

            if assigned_agent is not None:
                assigned_agent.current_task = None

            available_agents = [
                agent for agent in agents
                if agent.active and agent.current_task is None
            ]
            winner = self.allocate_task(available_agents, incident)

            if winner is not None:
                reassigned.append({
                    "incident_id": incident.incident_id,
                    "agent_id": winner.agent_id,
                })

        return reassigned
