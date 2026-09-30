from environment.grid import GridEnvironment
from environment.incidents import Incident
from agents.agent import Agent


def create_demo_scenario():
    grid = GridEnvironment(20, 20)

    # Static obstacles
    obstacles = [
        (5, 5), (5, 6), (5, 7),
        (10, 10), (11, 10), (12, 10),
        (14, 4), (14, 5)
    ]

    for position in obstacles:
        grid.add_obstacle(position)

    # Agents
    agents = [
    Agent("A1", (1, 1), ["ambulance"]),
    Agent("A2", (18, 1), ["ambulance"]),
    Agent("A3", (1, 18), ["fire_rescue"]),
    Agent("A4", (18, 18), ["ambulance", "fire_rescue"]),
    Agent("A5", (10, 18), ["ambulance", "fire_rescue"])
        ]

    # Emergency incidents
    incidents = [
        Incident("I1", (4, 4), 5, "ambulance"),
        Incident("I2", (16, 3), 4, "ambulance"),
        Incident("I3", (3, 16), 5, "fire_rescue"),
        Incident("I4", (15, 15), 3, "ambulance")
    ]

    for incident in incidents:
        grid.add_incident(incident)

    return grid, agents, incidents