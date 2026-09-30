from evaluation.metrics import SimulationMetrics


def test_metrics():
    metrics = SimulationMetrics()

    metrics.record_task_completion(10)
    metrics.record_task_completion(5)

    metrics.record_collision()
    metrics.record_replan()
    metrics.record_energy(20)
    metrics.record_latency(2.5)
    metrics.record_latency(3.5)

    summary = metrics.summary()

    assert summary["completed_tasks"] == 2
    assert summary["total_path_cost"] == 15
    assert summary["collisions"] == 1
    assert summary["replans"] == 1
    assert summary["energy_consumed"] == 20
    assert summary["average_latency_ms"] == 3.0
    assert "fitness" in summary