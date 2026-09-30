# Evaluation Attempt 2 Evidence

## Purpose

Attempt 2 evaluates the v2 implementation after targeted engineering changes based on Attempt 1 feedback.

## Changes

1. Adaptive decentralized task bidding
   - Added congestion, energy, communication-quality and local-load terms.
   - Added adaptive weight changes under stress.

2. Swarm-style congestion memory
   - Added a decaying local traffic field.
   - Integrated congestion into A* transition cost.

3. Time-aware trajectory coordination
   - Added edge-swap detection.
   - Added reservation-aware planning.
   - Added deterministic conflict priority and immediate waiting.

4. Runtime evidence
   - Added p50/p95/p99 latency measurements.
   - Added multi-scale benchmark cases.

5. Validation and documentation
   - Added regression tests for new coordination behavior.
   - Added technical architecture and benchmark documentation.

## What changed and why

> Attempt 2 changed the allocation and planning layers from a simple distance/urgency heuristic to adaptive, congestion-aware local coordination, and strengthened collision handling from vertex-only detection to time-aware vertex/edge conflict management. These changes directly target the autonomous-computing constraints identified during Attempt 1.

## Submission-machine verification

Fill these values only after running the current code locally:

```text
pytest:
<actual result>

demo scenario:
<actual result>

benchmark:
<actual benchmark output>

Attempt 2 evaluator score:
<paste actual score after evaluation>
```

Do not fabricate evaluator scores or benchmark measurements.
