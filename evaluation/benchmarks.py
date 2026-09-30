"""Repeatable runtime benchmark for PulseGrid's real-time decision loop."""

import time

from agents.agent import Agent
from environment.grid import GridEnvironment
from environment.incidents import Incident
from simulation.engine import SimulationEngine


def build_benchmark(agent_count, size):
    grid = GridEnvironment(size, size)
    agents = []

    for index in range(agent_count):
        x = index % size
        y = (index * 3) % size
        agents.append(
            Agent(
                f"A{index:03d}",
                (x, y),
                ["ambulance", "fire_rescue"],
            )
        )

    incidents = [
        Incident(
            f"I{index}",
            ((index * 7) % size, (index * 11) % size),
            severity=5 - (index % 3),
            resource_type="ambulance",
        )
        for index in range(min(agent_count, 20))
    ]

    for incident in incidents:
        if grid.is_walkable(incident.position):
            grid.add_incident(incident)

    engine = SimulationEngine(grid)
    for agent in agents:
        engine.add_agent(agent)

    engine.allocate_all_incidents(incidents)
    engine.start()

    return engine


def run_benchmark(agent_count=20, size=50, ticks=50):
    engine = build_benchmark(agent_count, size)

    start = time.perf_counter()
    for _ in range(ticks):
        engine.advance_tick()
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    latencies = engine.metrics.decision_latencies
    return {
        "agents": agent_count,
        "grid": f"{size}x{size}",
        "ticks": ticks,
        "wall_time_ms": round(elapsed_ms, 3),
        "p50_ms": round(engine.metrics.percentile_latency(50), 3),
        "p95_ms": round(engine.metrics.percentile_latency(95), 3),
        "p99_ms": round(engine.metrics.percentile_latency(99), 3),
        "completed_tasks": engine.metrics.completed_tasks,
        "collisions": engine.metrics.collisions,
        "deadlocks": engine.metrics.deadlocks,
    }


if __name__ == "__main__":
    cases = [
        (5, 20),
        (10, 30),
        (20, 50),
        (50, 75),
        (100, 100),
    ]

    print("PulseGrid Runtime Benchmark")
    print("=" * 72)
    for agent_count, size in cases:
        print(run_benchmark(agent_count, size))
