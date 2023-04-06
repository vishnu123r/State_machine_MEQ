import socket
from functions import count_key_dict, state_machine_viz
from random import randint

HOST = '20.28.230.252'
PORT = 65432
TERMINAL_STATE = 'Z'

state_list = [chr(i) for i in range(ord('A'), ord('Z')+1)]
number_of_states = len(state_list)
number_of_transitions = (number_of_states-1)*3
max_keys_state_machine = number_of_states + number_of_transitions + 1

state_machine = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    new_state = s.recv(1024).decode().strip()
    print("Initial state:", new_state)

    while count_key_dict(state_machine) <= max_keys_state_machine:
        request = str(randint(1,3))   
        s.sendall(request.encode() + b'\n')
        response = s.recv(1024).decode().strip()
        print("New state:", response)
        
        #Add to the state machine dictionary
        state_machine.setdefault(new_state,{}).update({request: response})
        new_state = response
        
        if new_state == TERMINAL_STATE:
                print("Reached terminal state Z. Restarting at state A.")
                s.sendall(b'A\n')
                new_state = s.recv(1024).decode().strip()
                print("New state:", new_state)
                if new_state != 'A':
                    print("Error: expected to receive state A after restarting. But {0}".format(new_state))
                    break
            
        elif new_state not in state_list:
            print("Error: invalid state received from server.")
            break
        
        
state_machine_viz(state_machine)