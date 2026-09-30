from agents.agent import Agent
from environment.incidents import Incident


def test_agent_creation():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    assert agent.agent_id == "A1"
    assert agent.position == (2, 3)
    assert "ambulance" in agent.capabilities
    assert agent.current_task is None
    assert agent.energy == 100.0
    assert agent.communication_available is True
    assert agent.active is True


def test_agent_capability():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    assert agent.can_handle("ambulance")
    assert not agent.can_handle("fire_unit")


def test_agent_task_assignment():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    incident = Incident(
        incident_id="I1",
        position=(10, 10),
        severity=5,
        resource_type="ambulance"
    )

    agent.assign_task(incident)

    assert agent.current_task == incident


def test_agent_failure():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    agent.fail()

    assert agent.active is False

def test_agent_path_assignment():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    path = [
        (2, 3),
        (3, 3),
        (4, 3),
        (4, 4)
    ]

    agent.set_path(path)

    assert agent.path == path

def test_agent_movement():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    path = [
        (2, 3),
        (3, 3),
        (4, 3)
    ]

    agent.set_path(path)

    agent.move_to_next_position()

    assert agent.position == (3, 3)
    assert agent.path == [(3, 3), (4, 3)]

    agent.move_to_next_position()

    assert agent.position == (4, 3)
    assert agent.path == [(4, 3)]


def test_failed_agent_does_not_move():
    agent = Agent(
        agent_id="A2",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    agent.set_path([
        (2, 3),
        (3, 3)
    ])

    agent.fail()
    agent.move_to_next_position()

    assert agent.position == (2, 3)

def test_communication_loss_and_restore():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    agent.lose_communication()
    assert agent.communication_available is False

    agent.restore_communication()
    assert agent.communication_available is True
