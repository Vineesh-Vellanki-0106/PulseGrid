from planning.collision_avoidance import CollisionDetector


def test_no_collision():
    detector = CollisionDetector()

    paths = {
        "A1": [(0, 0), (1, 0), (2, 0)],
        "A2": [(0, 1), (1, 1), (2, 1)]
    }

    conflicts = detector.detect_vertex_conflicts(paths)

    assert conflicts == []


def test_vertex_collision():
    detector = CollisionDetector()

    paths = {
        "A1": [(0, 0), (1, 0), (2, 0)],
        "A2": [(2, 0), (1, 0), (0, 0)]
    }

    conflicts = detector.detect_vertex_conflicts(paths)

    assert len(conflicts) == 1
    assert conflicts[0]["type"] == "vertex"
    assert conflicts[0]["tick"] == 1
    assert conflicts[0]["position"] == (1, 0)


def test_empty_path():
    detector = CollisionDetector()

    paths = {
        "A1": [],
        "A2": [(0, 0), (1, 0)]
    }

    conflicts = detector.detect_vertex_conflicts(paths)

    assert conflicts == []

def test_resolve_vertex_conflict():
    detector = CollisionDetector()

    paths = {
        "A1": [(2, 3), (2, 4), (2, 5)],
        "A2": [(2, 5), (2, 4), (2, 3)]
    }

    resolved = detector.resolve_vertex_conflicts(paths)

    assert len(resolved) == 1
    assert resolved[0]["position"] == (2, 4)
    assert resolved[0]["priority_agent"] == "A1"
    assert resolved[0]["waiting_agent"] == "A2"