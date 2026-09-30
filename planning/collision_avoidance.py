class CollisionDetector:
    """Detects vertex conflicts and edge-swap conflicts in time-indexed paths."""

    @staticmethod
    def _position_at(path, tick):
        if not path:
            return None
        return path[tick] if tick < len(path) else path[-1]

    def detect_vertex_conflicts(self, agent_paths):
        conflicts = []
        max_length = max(
            (len(path) for path in agent_paths.values()),
            default=0,
        )

        for tick in range(max_length):
            positions = {}
            for agent_id, path in agent_paths.items():
                position = self._position_at(path, tick)
                if position is None:
                    continue
                if position in positions:
                    conflicts.append({
                        "type": "vertex",
                        "tick": tick,
                        "position": position,
                        "agents": [positions[position], agent_id],
                    })
                else:
                    positions[position] = agent_id
        return conflicts

    def detect_edge_conflicts(self, agent_paths):
        conflicts = []
        agent_ids = sorted(agent_paths)

        max_length = max(
            (len(path) for path in agent_paths.values()),
            default=0,
        )

        for tick in range(1, max_length):
            for i, first_id in enumerate(agent_ids):
                first_path = agent_paths[first_id]
                first_prev = self._position_at(first_path, tick - 1)
                first_curr = self._position_at(first_path, tick)

                if first_prev is None or first_curr is None:
                    continue

                for second_id in agent_ids[i + 1:]:
                    second_path = agent_paths[second_id]
                    second_prev = self._position_at(second_path, tick - 1)
                    second_curr = self._position_at(second_path, tick)

                    if (
                        first_prev == second_curr
                        and second_prev == first_curr
                        and first_prev != first_curr
                    ):
                        conflicts.append({
                            "type": "edge",
                            "tick": tick,
                            "edge": (first_prev, first_curr),
                            "agents": [first_id, second_id],
                        })
        return conflicts

    def detect_conflicts(self, agent_paths):
        return (
            self.detect_vertex_conflicts(agent_paths)
            + self.detect_edge_conflicts(agent_paths)
        )

    def resolve_vertex_conflicts(self, agent_paths):
        resolved = []
        for conflict in self.detect_vertex_conflicts(agent_paths):
            priority_agent = min(conflict["agents"])
            waiting_agent = max(conflict["agents"])
            resolved.append({
                "type": conflict["type"],
                "tick": conflict["tick"],
                "position": conflict["position"],
                "priority_agent": priority_agent,
                "waiting_agent": waiting_agent,
            })
        return resolved

    def resolve_conflicts(self, agent_paths):
        resolved = []
        for conflict in self.detect_conflicts(agent_paths):
            priority_agent = min(conflict["agents"])
            waiting_agent = max(conflict["agents"])
            item = {
                "type": conflict["type"],
                "tick": conflict["tick"],
                "priority_agent": priority_agent,
                "waiting_agent": waiting_agent,
            }
            if conflict["type"] == "vertex":
                item["position"] = conflict["position"]
            else:
                item["edge"] = conflict["edge"]
            resolved.append(item)
        return resolved
