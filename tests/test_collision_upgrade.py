from planning.collision_avoidance import CollisionDetector

def test_edge_swap_detected():
    paths={'A1':[(0,0),(1,0)], 'A2':[(1,0),(0,0)]}
    conflicts=CollisionDetector().detect_edge_conflicts(paths)
    assert len(conflicts)==1
    assert conflicts[0]['type']=='edge'

def test_vertex_conflict_detected():
    paths={'A1':[(0,0),(1,0)], 'A2':[(2,0),(1,0)]}
    conflicts=CollisionDetector().detect_vertex_conflicts(paths)
    assert len(conflicts)==1
