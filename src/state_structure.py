import socket
import pprint
import random
from graphviz import Digraph

class StateMachineStructure:
    def __init__(self, host, port, terminal_state = 'Z'):
        self.host = host
        self.port = port
        self.terminal_state = terminal_state
        
        # Determine the number of states and transitions
        self.state_list = [chr(i) for i in range(ord('A'), ord('Z')+1)]
        self.number_of_states = len(self.state_list)
        self.number_of_transitions = (self.number_of_states-1)*3
        self.max_keys_state_machine = self.number_of_states + self.number_of_transitions + 1
        
        #Intialise the state machine dictionary
        self.state_machine = {state:{} for state in self.state_list}
        self.state_machine.setdefault(self.terminal_state, {}).setdefault('', 'A')

    def _count_key_dict(self, dictionary):
        "This returns the number of keys in a nested dictionary"
        count = len(dictionary)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                count += self._count_key_dict(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        count += self._count_key_dict(item)
        
        return count

    def _request_strategy_1(self):
        """
        This strategy will always choose a random transition.
        """
        request = str(random.randint(1,3))
        return request
    
    def _request_strategy_2(self, state_machine, new_state):
        """
        This strategy will always choose a transition that has not been explored yet for a given state. 
        However, if all transitions have been explored, it will choose a random transition.
        """
        
        POSSIBLE_TRANSITIONS = {'1', '2', '3'}
        explored_transitions = set(state_machine[new_state].keys())
        unexplored_transitions = POSSIBLE_TRANSITIONS - explored_transitions
        if len(unexplored_transitions) == 0:
            request = str(random.randint(1,3)) 
        else:
            request = random.sample(unexplored_transitions, 1)[0]
        return request

    def _visualize_state_machine(self, state_machine):
        """
        This function visulises the state machine dictionary as a directed graph.
        """
        graph = Digraph()
        graph.attr(rankdir='LR')
    
        state_list = list(state_machine.keys())
        for state in state_list:
            graph.node(state)
        
        for start_state in state_machine:
            transition_dict = state_machine[start_state]
            for action in list(transition_dict.keys()):
                end_state = transition_dict[action]
                graph.edge(start_state, end_state, label=action)
        
        graph.render('state_machine_structure.gv', view=True)

    def run(self, request_strategy = 2):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            new_state = s.recv(1024).decode().strip()
            no_of_requests = 0

            while self._count_key_dict(self.state_machine) < self.max_keys_state_machine:
                no_of_requests += 1
                comp = 100*(self._count_key_dict(self.state_machine))/self.max_keys_state_machine

                # Update status
                print("\r%d%% completed" % comp, end='', flush=True)

                # Set request strategy
                if request_strategy == 1:
                    request = self._request_strategy_1()
                elif request_strategy == 2:
                    request = self._request_strategy_2(self.state_machine, new_state)
                    
                s.sendall(request.encode() + b'\n')
                response = s.recv(1024).decode().strip()

                #Add to the state machine dictionary
                self.state_machine.setdefault(new_state,{}).setdefault(request,response)
                new_state = response

                if new_state == self.terminal_state:
                    s.sendall(b'A\n')
                    new_state = s.recv(1024).decode().strip()
                    if new_state != 'A':
                        print(f"Error: expected to receive state A after restarting. But received state {new_state}")
                        break

                elif new_state not in self.state_list:
                    print(f"Error: invalid state received from server - {new_state}.")
                    break

            print("\r100% completed")
            print(f"The structure has been determined after {no_of_requests} requests. Please refer to the state_machine.gv file for the state machine diagram.")          
            print("The state machine dictionary is:")
            pprint.pprint(self.state_machine)

            # Save and open the state_machine.gv file
            self._visualize_state_machine(self.state_machine)

if __name__ == '__main__':
    HOST = '20.28.230.252'
    PORT = 65432

    sm = StateMachineStructure(HOST, PORT)
    sm.run()