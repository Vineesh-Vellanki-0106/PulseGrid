class CollisionDetector:
    def detect_vertex_conflicts(self, agent_paths):
        conflicts = []

        max_length = max(
            (len(path) for path in agent_paths.values()),
            default=0
        )

        for tick in range(max_length):
            positions = {}

            for agent_id, path in agent_paths.items():
                if not path:
                    continue

                position = (
                    path[tick]
                    if tick < len(path)
                    else path[-1]
                )

                if position in positions:
                    conflicts.append({
                        "type": "vertex",
                        "tick": tick,
                        "position": position,
                        "agents": [
                            positions[position],
                            agent_id
                        ]
                    })
                else:
                    positions[position] = agent_id

        return conflicts
    
    def resolve_vertex_conflicts(self, agent_paths):
        conflicts = self.detect_vertex_conflicts(agent_paths)
        resolved = []

        for conflict in conflicts:
            agents = conflict["agents"]

            # Lower agent ID gets priority deterministically.
            priority_agent = min(agents)
            waiting_agent = max(agents)

            resolved.append({
                "tick": conflict["tick"],
                "position": conflict["position"],
                "priority_agent": priority_agent,
                "waiting_agent": waiting_agent
            })

        return resolved


        