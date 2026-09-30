from evaluation.benchmarks import run_benchmark

def test_benchmark_smoke():
    result=run_benchmark(agent_count=5,size=20,ticks=5)
    assert result['agents']==5
    assert result['ticks']==5
    assert result['p95_ms'] >= 0
