from environment.grid import GridEnvironment
from environment.incidents import Incident

def test_grid_creation():
    grid = GridEnvironment(20, 20)

    assert grid.width == 20
    assert grid.height == 20
    assert len(grid.obstacles) == 0


def test_position_validation():
    grid = GridEnvironment(20, 20)

    assert grid.is_valid_position((0, 0))
    assert grid.is_valid_position((19, 19))

    assert not grid.is_valid_position((-1, 0))
    assert not grid.is_valid_position((20, 20))


def test_obstacle():
    grid = GridEnvironment(20, 20)

    grid.add_obstacle((5, 5))

    assert (5, 5) in grid.obstacles
    assert not grid.is_walkable((5, 5))
    assert grid.is_walkable((5, 6))


def test_add_incident():
    grid = GridEnvironment(20, 20)

    incident = Incident(
        incident_id="I1",
        position=(10, 15),
        severity=5,
        resource_type="ambulance"
    )

    grid.add_incident(incident)

    assert "I1" in grid.incidents
    assert grid.incidents["I1"] == incident

    
def test_remove_obstacle():
    grid = GridEnvironment(20, 20)

    grid.add_obstacle((5, 5))
    assert (5, 5) in grid.obstacles
    assert not grid.is_walkable((5, 5))

    grid.remove_obstacle((5, 5))

    assert (5, 5) not in grid.obstacles
    assert grid.is_walkable((5, 5))