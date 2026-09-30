class TaskAllocator:
    def calculate_cost(self, agent, incident):
        if not agent.active:
            return float("inf")

        if not agent.communication_available:
            return float("inf")

        if not agent.can_handle(incident.resource_type):
            return float("inf")

        distance = abs(
            agent.position[0] - incident.position[0]
        ) + abs(
            agent.position[1] - incident.position[1]
        )

        urgency_penalty = (6 - incident.severity) * 5

        energy_penalty = (100 - agent.energy) * 0.1

        total_cost = (
            distance
            + urgency_penalty
            + energy_penalty
        )

        return total_cost
    
    def collect_bids(self, agents, incident):
        bids = []

        for agent in agents:
            cost = self.calculate_cost(agent, incident)

            if cost != float("inf"):
                bids.append({
                    "agent_id": agent.agent_id,
                    "cost": cost
                })

        return bids
    def select_winner(self, bids):
        if not bids:
            return None

        return min(
            bids,
            key=lambda bid: bid["cost"]
        )
    def allocate_task(self, agents, incident):
        bids = self.collect_bids(agents, incident)

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

        for incident in incidents:
            available_agents = [
                agent
                for agent in agents
                if agent.active and agent.current_task is None
            ]

            if not available_agents:
                break

            winner = self.allocate_task(
                available_agents,
                incident
            )

            if winner is not None:
                assignments.append({
                    "incident_id": incident.incident_id,
                    "agent_id": winner.agent_id
                })

        return assignments
    
    def reassign_failed_tasks(self, agents, incidents):
        reassigned = []

        for incident in incidents:
            if incident.completed:
                continue

            assigned_agent = None

            for agent in agents:
                if agent.current_task == incident:
                    assigned_agent = agent
                    break

            if assigned_agent is not None and assigned_agent.active:
                continue

            if assigned_agent is not None:
                assigned_agent.current_task = None

            available_agents = [
                agent
                for agent in agents
                if agent.active and agent.current_task is None
            ]

            if not available_agents:
                continue

            winner = self.allocate_task(
                available_agents,
                incident
            )

            if winner is not None:
                reassigned.append({
                    "incident_id": incident.incident_id,
                    "agent_id": winner.agent_id
                })

        return reassigned