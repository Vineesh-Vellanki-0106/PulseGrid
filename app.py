from simulation.engine import SimulationEngine
from simulation.scenarios import create_demo_scenario


def main():
    grid, agents, incidents = create_demo_scenario()

    engine = SimulationEngine(grid)

    for agent in agents:
        engine.add_agent(agent)

    assignments = engine.allocate_all_incidents(incidents)

    print("\n" + "=" * 60)
    print("PULSEGRID — DECENTRALIZED EMERGENCY RESPONSE")
    print("=" * 60)

    print("\nINITIAL ALLOCATION")

    for assignment in assignments:
        print(
            f"{assignment['agent_id']} -> "
            f"{assignment['incident_id']}"
        )

    # IMPORTANT
    engine.start()

    print("\nSIMULATION STARTED")

    for _ in range(30):

        # Dynamic obstacle
        if engine.tick == 2:
            print("\n[EVENT] Dynamic obstacle detected")
            grid.add_obstacle((1, 4))

        # Communication dropout
        if engine.tick == 3:
            print("\n[EVENT] A2 communication lost")
            agents[1].lose_communication()

        # Agent failure
        if engine.tick == 4:
            print("\n[EVENT] A3 FAILED")

            agents[2].fail()

            reassigned = engine.reassign_failed_tasks(
                incidents
            )

            for event in reassigned:
                print(
                    f"[RECOVERY] "
                    f"{event['incident_id']} -> "
                    f"{event['agent_id']}"
                )

        # Advance simulation
        engine.advance_tick()

        print(
            f"\nTICK {engine.tick} | "
            f"LATENCY "
            f"{engine.metrics.average_latency():.3f} ms"
        )

        for agent in agents:
            task_id = (
                agent.current_task.incident_id
                if agent.current_task
                else "NONE"
            )

            print(
                f"{agent.agent_id}: "
                f"position={agent.position} | "
                f"TASK={task_id} | "
                f"ACTIVE={agent.active} | "
                f"COMM={agent.communication_available}"
            )

        if all(incident.completed for incident in incidents):
            print("\nALL INCIDENTS COMPLETED")
            break

    engine.stop()

    print("\n" + "=" * 60)
    print("FINAL PERFORMANCE")
    print("=" * 60)

    for key, value in engine.metrics.summary().items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()