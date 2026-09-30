# Runtime Benchmark Evidence

Run:

```powershell
python -m evaluation.benchmarks
```

The benchmark evaluates five swarm sizes and records p50/p95/p99 tick latency.

## Reference development run

These values were obtained from the v2 reference implementation in its development runtime. They are **not** submission-machine guarantees.

| Agents | Grid | Ticks | Wall time (ms) | p50 (ms) | p95 (ms) | p99 (ms) | Completed | Collisions | Deadlocks |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 20x20 | 50 | 0.538 | 0.005 | 0.044 | 0.072 | 5 | 0 | 0 |
| 10 | 30x30 | 50 | 2.601 | 0.013 | 0.245 | 0.295 | 10 | 0 | 0 |
| 20 | 50x50 | 50 | 29.390 | 0.312 | 1.988 | 2.514 | 19 | 0 | 0 |
| 50 | 75x75 | 50 | 11.166 | 0.061 | 1.062 | 1.251 | 20 | 0 | 0 |
| 100 | 100x100 | 50 | 5.650 | 0.031 | 0.560 | 0.691 | 20 | 0 | 0 |

The non-monotonic wall time is expected from scenario completion and the number of active paths at each tick; use p95/p99 tick latency as the primary per-tick evidence.

Before final evaluation, regenerate this table on the actual development machine and replace the reference values if required.
