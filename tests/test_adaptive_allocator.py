from agents.agent import Agent
from agents.task_allocator import TaskAllocator
from environment.grid import GridEnvironment
from environment.incidents import Incident

def test_adaptive_allocator_prefers_capable_active_agent():
    env=GridEnvironment(10,10)
    planner=None
    allocator=TaskAllocator(env,planner)
    a1=Agent('A1',(0,0),['ambulance'])
    a2=Agent('A2',(8,8),['fire_rescue'])
    inc=Incident('I1',(1,0),5,'ambulance')
    winner=allocator.allocate_task([a1,a2],inc)
    assert winner.agent_id=='A1'

def test_communication_loss_excludes_agent():
    env=GridEnvironment(10,10)
    allocator=TaskAllocator(env,None)
    a1=Agent('A1',(0,0),['ambulance']); a1.lose_communication()
    a2=Agent('A2',(5,5),['ambulance'])
    inc=Incident('I1',(1,0),5,'ambulance')
    assert allocator.allocate_task([a1,a2],inc).agent_id=='A2'
