from environment.grid import GridEnvironment
from planning.astar import AStarPlanner


def test_basic_path():
    grid = GridEnvironment(10, 10)
    planner = AStarPlanner(grid)

    path = planner.find_path((0, 0), (4, 4))

    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)
    assert len(path) == 9


def test_path_avoids_obstacle():
    grid = GridEnvironment(10, 10)

    grid.add_obstacle((1, 0))
    grid.add_obstacle((1, 1))
    grid.add_obstacle((1, 2))

    planner = AStarPlanner(grid)

    path = planner.find_path((0, 0), (2, 0))

    assert path[0] == (0, 0)
    assert path[-1] == (2, 0)

    for position in path:
        assert position not in grid.obstacles


def test_invalid_start():
    grid = GridEnvironment(10, 10)
    grid.add_obstacle((0, 0))

    planner = AStarPlanner(grid)

    path = planner.find_path((0, 0), (5, 5))

    assert path == []


def test_invalid_goal():
    grid = GridEnvironment(10, 10)
    grid.add_obstacle((5, 5))

    planner = AStarPlanner(grid)

    path = planner.find_path((0, 0), (5, 5))

    assert path == []