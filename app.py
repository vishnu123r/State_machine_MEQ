from src.state_structure import StateMachineStructure

HOST = '20.28.230.252'
PORT = 65432

sm = StateMachineStructure(HOST, PORT)
sm.run()