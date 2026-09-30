# PulseGrid v2 — Adaptive Swarm Coordination

## Why v2

The first evaluation established a strong validation baseline but exposed gaps in adaptive coordination, trajectory-level conflict handling, runtime evidence, and technical documentation. v2 addresses those gaps without replacing the core architecture.

## Adaptive decentralized bidding

The allocator now supports a context-aware local bid function using:

- travel distance
- incident severity / urgency
- agent energy state
- communication quality
- local congestion
- local workload / path pressure
- adaptive weight changes under swarm stress

The simulation engine supplies the environment and planner so the deployed simulation uses the adaptive path rather than only the legacy baseline cost.

## Congestion-aware swarm memory

The grid maintains a decaying congestion field. Agents add local traffic information as they move. A* can include congestion in its transition cost, creating a lightweight stigmergic coordination mechanism: recently used areas become less attractive to other agents while the field decays over time.

## Time-aware trajectory coordination

Collision handling now considers:

1. vertex conflicts — two agents occupying the same cell at the same time;
2. edge conflicts — two agents swapping positions during the same transition;
3. deterministic priority resolution for reproducibility;
4. reservation-aware A* planning;
5. wait/replan behavior for immediate conflicts.

This is stronger than checking only spatial overlap after paths have been generated.

## Runtime evidence

`evaluation/benchmarks.py` provides repeatable measurements across multiple swarm sizes and grid sizes and reports:

- wall-clock runtime
- p50 tick latency
- p95 tick latency
- p99 tick latency
- completed tasks
- collisions
- deadlocks

Latency measurements are hardware-dependent and should be regenerated on the submission machine before being presented as final benchmark evidence.

## Validation

The v2 upgrade adds regression coverage for:

- edge-swap collision detection
- deterministic conflict priority
- congestion-sensitive bidding
- communication-quality-sensitive bidding
- benchmark output and percentile ordering

Existing public APIs were retained where practical so the original project tests remain compatible.

## Engineering honesty

PulseGrid does not claim a formal mathematical proof of global collision freedom or optimality. It implements deterministic local coordination, reservation-aware planning, adaptive heuristic allocation, and runtime validation. The system is intended as a reproducible autonomous-computing prototype rather than a certified emergency-response controller.
