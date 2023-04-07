import socket
import pprint
import random
from graphviz import Digraph
import datetime
import sys

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
       
        return count

    def _request_strategy_1(self):
        """
        This strategy will choose a random transition.
        """
        return str(random.randint(1,3))
    
    def _request_strategy_2(self, state_machine, new_state):
        """
        This strategy will always choose a transition that has not been explored yet for a given state. 
        However, if all transitions have been explored, it will choose a random transition.
        """
        
        POSSIBLE_TRANSITIONS = {'1', '2', '3'}
        explored_transitions = set(state_machine[new_state].keys())
        unexplored_transitions = POSSIBLE_TRANSITIONS - explored_transitions
        if len(unexplored_transitions) == 0:
            return str(random.randint(1,3))
        
        return random.sample(unexplored_transitions, 1)[0]

    def _visualize_state_machine(self, state_machine):
        """
        This function visualises the state machine dictionary as a directed graph.
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
        
        #Add time stamp to the file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f'img/state_machine_structure_{timestamp}.gv'
        try:
            graph.render(file_name, view=True)
        except Exception as e:
            print(f"Error: {e}. Please Install Graphviz and add it to the PATH environment variable to view the state machine diagram.")
    
    def _connect_to_server(self):
        """
        This function connects to the server and returns the client socket object.
        """
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))
            return client
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(f"Please check if the server is running on {self.host}:{self.port}")
    
    def _send_request(self, client, request_func, new_state):
        """
        send request to server and return response
        """
        request = request_func(self.state_machine, new_state)
        client.sendall(request.encode() + b'\n')
        response = client.recv(1024).decode().strip()
        
        return request, response
    
    def _update_state_machine(self, new_state, request, response):
        """
        Updates state machine dictionary with the new state, request and response
        """
        self.state_machine.setdefault(new_state,{}).setdefault(request,response)
        
        return response
    
    def _handle_terminal_state(self, client, new_state ):
        
        """     
        Handles the terminal state 'Z' by sending a new line character and receiving the new state. Ensures that the new state is 'A'.
        """
        if new_state == self.terminal_state:
            client.sendall(b'\n')
            new_state = client.recv(1024).decode().strip()
            if new_state != 'A':
                raise ValueError(f"Expected to receive state A after restarting. But received state {new_state}")
        
        return new_state
    
    
    def _handle_invalid_state(self, new_state):
        """
        Raises error if the new state received from the server is not in the state list.
        """
        if new_state not in self.state_list:
            raise ValueError(f"Invalid state received from server - {new_state}")
      
    def run(self, request_strategy = 2):
        with self._connect_to_server() as client:
            print(f"Connected to {self.host}:{self.port}")
            new_state = client.recv(1024).decode().strip()
            no_of_requests = 0

            print("Determining the structure of the state machine...")
            
            while self._count_key_dict(self.state_machine) < self.max_keys_state_machine:
                no_of_requests += 1
                
                # Update status log
                comp = 100*(self._count_key_dict(self.state_machine))/self.max_keys_state_machine
                print("\r%d%% completed" % comp, end='', flush=True)

                request_func = self._request_strategy_1 if request_strategy == 1 else self._request_strategy_2
                request, response = self._send_request(client, request_func, new_state)
                new_state = self._update_state_machine(new_state, request, response)
                new_state = self._handle_terminal_state(client, new_state)
                self._handle_invalid_state(new_state)


            print("\r100% completed")
            print(f"The structure has been determined after {no_of_requests} requests. Please refer to the state_machine.gv saved in the img folder file for the state machine diagram.")          
            print("The state machine dictionary is:")
            pprint.pprint(self.state_machine)
        
            # Save and open the state_machine.gv file
            self._visualize_state_machine(self.state_machine)
