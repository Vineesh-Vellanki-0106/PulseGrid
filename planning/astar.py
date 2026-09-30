import heapq


class AStarPlanner:
    """A* planner with optional congestion and time-reservation costs."""

    def __init__(self, environment):
        self.environment = environment

    def heuristic(self, current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, position):
        x, y = position
        candidates = [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1)
        ]
        return [
            neighbor for neighbor in candidates
            if self.environment.is_walkable(neighbor)
        ]

    def _reserved(self, reservations, position, tick):
        return position in reservations.get(tick, set())

    def _edge_reserved(self, edge_reservations, start, end, tick):
        return (start, end) in edge_reservations.get(tick, set())

    def find_path(
        self,
        start,
        goal,
        reservations=None,
        edge_reservations=None,
        congestion_weight=0.0,
        max_time=None,
    ):
        if not self.environment.is_walkable(start):
            return []
        if not self.environment.is_walkable(goal):
            return []

        reservations = reservations or {}
        edge_reservations = edge_reservations or {}
        if max_time is None:
            max_time = self.environment.width * self.environment.height * 4

        # State includes time so agents can wait for reservations.
        open_set = []
        heapq.heappush(open_set, (self.heuristic(start, goal), 0.0, start, 0))
        came_from = {}
        cost_so_far = {(start, 0): 0.0}

        while open_set:
            _, current_cost, current, tick = heapq.heappop(open_set)

            if current == goal:
                return self._reconstruct_path(came_from, (current, tick))

            if tick >= max_time:
                continue

            next_tick = tick + 1
            candidates = self.get_neighbors(current) + [current]

            for neighbor in candidates:
                if not self.environment.is_walkable(neighbor):
                    continue

                if self._reserved(reservations, neighbor, next_tick):
                    continue

                if self._edge_reserved(
                    edge_reservations, current, neighbor, next_tick
                ):
                    continue

                congestion = self.environment.get_congestion(neighbor)
                step_cost = 1.0 + congestion_weight * congestion
                new_cost = current_cost + step_cost
                state = (neighbor, next_tick)

                if new_cost < cost_so_far.get(state, float("inf")):
                    cost_so_far[state] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(
                        open_set,
                        (priority, new_cost, neighbor, next_tick),
                    )
                    came_from[state] = (current, tick)

        return []

    def _reconstruct_path(self, came_from, current_state):
        path = [current_state[0]]
        while current_state in came_from:
            current_state = came_from[current_state]
            path.append(current_state[0])
        path.reverse()
        return path
