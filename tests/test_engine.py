from environment.grid import GridEnvironment
from simulation.engine import SimulationEngine
from agents.agent import Agent
from environment.incidents import Incident

def test_engine_creation():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    assert engine.environment == grid
    assert engine.agents == []
    assert engine.tick == 0
    assert engine.running is False


def test_add_agent():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    engine.add_agent(agent)

    assert len(engine.agents) == 1
    assert engine.agents[0] == agent


def test_simulation_ticks():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    engine.start()

    engine.advance_tick()
    engine.advance_tick()
    engine.advance_tick()

    assert engine.tick == 3


def test_stopped_engine_does_not_advance():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    engine.advance_tick()

    assert engine.tick == 0


def test_assign_path():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    engine.add_agent(agent)

    result = engine.assign_path(agent, (6, 3))

    assert result is True
    assert agent.path[0] == (2, 3)
    assert agent.path[-1] == (6, 3)
def test_agent_moves_during_simulation():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    engine.add_agent(agent)

    engine.assign_path(agent, (6, 3))

    engine.start()

    engine.advance_tick()

    assert engine.tick == 1
    assert agent.position == (3, 3)

def test_engine_detects_collision():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    agent1 = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    agent2 = Agent(
        agent_id="A2",
        position=(2, 5),
        capabilities=["ambulance"]
    )

    engine.add_agent(agent1)
    engine.add_agent(agent2)

    agent1.set_path([
        (2, 3),
        (2, 4),
        (2, 5)
    ])

    agent2.set_path([
        (2, 5),
        (2, 4),
        (2, 3)
    ])

    collisions = engine.detect_collisions()

    assert len(collisions) == 1
    assert collisions[0]["type"] == "vertex"
    assert collisions[0]["tick"] == 1
    assert collisions[0]["position"] == (2, 4)

def test_replan_when_path_is_blocked():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    engine.add_agent(agent)

    destination = (6, 3)

    # Initial path
    assert engine.assign_path(agent, destination) is True
    original_path = agent.path.copy()

    # Introduce a dynamic obstacle on the route
    blocked_position = original_path[2]
    grid.add_obstacle(blocked_position)

    # Agent should calculate a new route
    assert engine.replan_if_blocked(agent, destination) is True

    assert agent.path != original_path
    assert blocked_position not in agent.path
    assert agent.path[-1] == destination

def test_allocate_incident():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    agent1 = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    agent2 = Agent(
        agent_id="A2",
        position=(15, 15),
        capabilities=["ambulance"]
    )

    engine.add_agent(agent1)
    engine.add_agent(agent2)

    incident = Incident(
        incident_id="I1",
        position=(5, 3),
        severity=5,
        resource_type="ambulance"
    )

    winner = engine.allocate_incident(incident)

    assert winner is agent1
    assert agent1.current_task == incident
    assert agent1.path[0] == (2, 3)
    assert agent1.path[-1] == (5, 3)

    assert agent2.current_task is None

def test_resolve_collisions():
    grid = GridEnvironment(20, 20)
    engine = SimulationEngine(grid)

    agent1 = Agent("A1", (2, 3), ["ambulance"])
    agent2 = Agent("A2", (2, 5), ["ambulance"])

    engine.add_agent(agent1)
    engine.add_agent(agent2)

    agent1.set_path([
        (2, 3),
        (2, 4),
        (2, 5)
    ])

    agent2.set_path([
        (2, 5),
        (2, 4),
        (2, 3)
    ])

    waiting = engine.resolve_collisions()

    assert "A2" in waiting
    assert "A1" not in waiting

def test_allocate_all_incidents():
    from simulation.scenarios import create_demo_scenario

    grid, agents, incidents = create_demo_scenario()

    engine = SimulationEngine(grid)

    for agent in agents:
        engine.add_agent(agent)

    assignments = engine.allocate_all_incidents(incidents)

    assert len(assignments) == 4

    assigned_agents = {
        assignment["agent_id"]
        for assignment in assignments
    }

    assigned_incidents = {
        assignment["incident_id"]
        for assignment in assignments
    }

    assert len(assigned_agents) == 4
    assert assigned_incidents == {"I1", "I2", "I3", "I4"}

    # Exactly four agents should have active tasks.
    active_task_agents = [
        agent
        for agent in agents
        if agent.current_task is not None
    ]

    assert len(active_task_agents) == 4

    # A5 is intentionally reserved for failure recovery.
    reserve_agent = next(
        agent
        for agent in agents
        if agent.agent_id == "A5"
    )

    assert reserve_agent.current_task is None