from agents.agent import Agent
from environment.incidents import Incident
from agents.task_allocator import TaskAllocator


def test_calculate_task_cost():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    incident = Incident(
        incident_id="I1",
        position=(5, 7),
        severity=5,
        resource_type="ambulance"
    )

    allocator = TaskAllocator()

    cost = allocator.calculate_cost(agent, incident)

    # Manhattan distance = 7
    # Urgency penalty = (6 - 5) * 5 = 5
    # Energy penalty = 0
    assert cost == 12


def test_incompatible_agent_gets_infinite_cost():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["fire_rescue"]
    )

    incident = Incident(
        incident_id="I1",
        position=(5, 7),
        severity=5,
        resource_type="ambulance"
    )

    allocator = TaskAllocator()

    cost = allocator.calculate_cost(agent, incident)

    assert cost == float("inf")


def test_failed_agent_gets_infinite_cost():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    agent.fail()

    incident = Incident(
        incident_id="I1",
        position=(5, 7),
        severity=5,
        resource_type="ambulance"
    )

    allocator = TaskAllocator()

    cost = allocator.calculate_cost(agent, incident)

    assert cost == float("inf")

def test_collect_bids():
    agents = [
        Agent(
            agent_id="A1",
            position=(2, 3),
            capabilities=["ambulance"]
        ),
        Agent(
            agent_id="A2",
            position=(10, 10),
            capabilities=["ambulance"]
        ),
        Agent(
            agent_id="A3",
            position=(5, 5),
            capabilities=["fire_rescue"]
        )
    ]

    incident = Incident(
        incident_id="I1",
        position=(5, 3),
        severity=5,
        resource_type="ambulance"
    )

    allocator = TaskAllocator()

    bids = allocator.collect_bids(agents, incident)

    assert len(bids) == 2

    assert bids[0]["agent_id"] == "A1"
    assert bids[1]["agent_id"] == "A2"

    assert bids[0]["cost"] < bids[1]["cost"]
def test_select_winner():
    allocator = TaskAllocator()

    bids = [
        {"agent_id": "A1", "cost": 12},
        {"agent_id": "A2", "cost": 18},
        {"agent_id": "A4", "cost": 9}
    ]

    winner = allocator.select_winner(bids)

    assert winner["agent_id"] == "A4"
    assert winner["cost"] == 9
def test_select_winner_with_no_bids():
    allocator = TaskAllocator()

    winner = allocator.select_winner([])

    assert winner is None


def test_allocate_task():
    agents = [
        Agent(
            agent_id="A1",
            position=(2, 3),
            capabilities=["ambulance"]
        ),
        Agent(
            agent_id="A2",
            position=(10, 10),
            capabilities=["ambulance"]
        )
    ]

    incident = Incident(
        incident_id="I1",
        position=(5, 3),
        severity=5,
        resource_type="ambulance"
    )

    allocator = TaskAllocator()

    winner = allocator.allocate_task(agents, incident)

    assert winner is agents[0]
    assert agents[0].current_task == incident
    assert agents[1].current_task is None

def test_allocate_multiple_tasks():
    agents = [
        Agent("A1", (2, 3), ["ambulance"]),
        Agent("A2", (15, 15), ["ambulance"]),
        Agent("A3", (10, 2), ["ambulance"])
    ]

    incidents = [
        Incident("I1", (3, 3), 5, "ambulance"),
        Incident("I2", (14, 15), 4, "ambulance"),
        Incident("I3", (10, 3), 3, "ambulance")
    ]

    allocator = TaskAllocator()

    assignments = allocator.allocate_tasks(
        agents,
        incidents
    )

    assert len(assignments) == 3

    assigned_agents = {
        assignment["agent_id"]
        for assignment in assignments
    }

    assigned_incidents = {
        assignment["incident_id"]
        for assignment in assignments
    }

    assert len(assigned_agents) == 3
    assert assigned_incidents == {"I1", "I2", "I3"}

def test_reassign_failed_task():
    agents = [
        Agent("A1", (2, 3), ["ambulance"]),
        Agent("A2", (10, 10), ["ambulance"])
    ]

    incident = Incident(
        "I1",
        (5, 3),
        5,
        "ambulance"
    )

    allocator = TaskAllocator()

    allocator.allocate_task(agents, incident)

    assert agents[0].current_task == incident

    agents[0].fail()

    reassigned = allocator.reassign_failed_tasks(
        agents,
        [incident]
    )

    assert len(reassigned) == 1
    assert reassigned[0]["agent_id"] == "A2"
    assert agents[1].current_task == incident

def test_disconnected_agent_gets_infinite_cost():
    agent = Agent(
        agent_id="A1",
        position=(2, 3),
        capabilities=["ambulance"]
    )

    agent.communication_available = False

    incident = Incident(
        incident_id="I1",
        position=(5, 3),
        severity=5,
        resource_type="ambulance"
    )

    allocator = TaskAllocator()

    cost = allocator.calculate_cost(agent, incident)

    assert cost == float("inf")