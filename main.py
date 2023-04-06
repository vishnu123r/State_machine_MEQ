import socket
from functions import count_key_dict, visualise_state_machine, request_strategy_1, request_strategy_2
import random
from sys import stdout

HOST = '20.28.230.252'
PORT = 65432
TERMINAL_STATE = 'Z'

state_list = [chr(i) for i in range(ord('A'), ord('Z')+1)]
number_of_states = len(state_list)
number_of_transitions = (number_of_states-1)*3
max_keys_state_machine = number_of_states + number_of_transitions + 1

#Intialise the state machine dictionary
state_machine = {}
for state in state_list:
    state_machine[state] = {}
state_machine.setdefault('Z',{}).setdefault('','A')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    new_state = s.recv(1024).decode().strip()
    no_of_requests = 0
    
    while count_key_dict(state_machine) < max_keys_state_machine:
        no_of_requests += 1
        comp = 100*(count_key_dict(state_machine))/max_keys_state_machine

        # Update status
        stdout.write("\r%d%% completed" % comp)
        stdout.flush()
        
        request = request_strategy_2(state_machine, new_state)
        s.sendall(request.encode() + b'\n')
        response = s.recv(1024).decode().strip()
        
        #Add to the state machine dictionary
        state_machine.setdefault(new_state,{}).setdefault(request,response)
        new_state = response
        
        if new_state == TERMINAL_STATE:
                s.sendall(b'A\n')
                new_state = s.recv(1024).decode().strip()
                if new_state != 'A':
                    print(f"Error: expected to recieve state A after restarting. But recived state {new_state}")
                    break
            
        elif new_state not in state_list:
            print(f"Error: invalid state received from server - {new_state}.")
            break

    
stdout. write("\033[F")# Go previous line
stdout. write("\033[K") #Delete the line
stdout.write("100% " + "completed")
stdout.write("\n")
print(f"The structure has been determined after {no_of_requests} requests. Please refer to the state_machine.gv file for the state machine diagram.")          

### Save and open the state_machine.gv file
visualise_state_machine(state_machine)