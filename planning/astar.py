import heapq


class AStarPlanner:
    def __init__(self, environment):
        self.environment = environment

    def heuristic(self, current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, position):
        x, y = position

        candidates = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        return [
            neighbor
            for neighbor in candidates
            if self.environment.is_walkable(neighbor)
        ]

    def find_path(self, start, goal):
        if not self.environment.is_walkable(start):
            return []

        if not self.environment.is_walkable(goal):
            return []

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self._reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1

                if (
                    neighbor not in cost_so_far
                    or new_cost < cost_so_far[neighbor]
                ):
                    cost_so_far[neighbor] = new_cost

                    priority = (
                        new_cost
                        + self.heuristic(neighbor, goal)
                    )

                    heapq.heappush(
                        open_set,
                        (priority, neighbor)
                    )

                    came_from[neighbor] = current

        return []

    def _reconstruct_path(self, came_from, current):
        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path