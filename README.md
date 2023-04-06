# App to determine the state machine structure
This program connects to a server over a socket and requests data to to determine the structure of a randomly created state machine. The state machine is represented by a dictionary, where the keys are the states and the values are dictionaries that represent the transitions. The program determines the structure of the state machine, and visualizes the resulting state machine using Graphviz.

## Requirements
Python 3.x
Graphviz

## Installation
Clone the repository: git clone https://github.com/vishnu123r/State_machine_MEQ.git
Install the required packages: pip install -r requirements.txt

## Usage
Open a terminal and navigate to the directory where the program is located.
Run the program: python app.py
Wait for the program to finish running.
The resulting state machine diagram will be saved to the state_machine.gv file in the same directory.

## Functionality
The program does the following:
- Imports necessary libraries and functions.
- Initializes constants and creates the initial state machine dictionary.
- Connects to the server using a socket and receives the initial state.
- Loops while the number of keys in the state machine is less than the maximum number of keys.
- Uses one of two request strategies to send a request to the server and receive a response.
- Adds the new transition to the state machine dictionary.
- Checks for errors in the response and breaks the loop if an error occurs.
- Updates the current state based on the response.
- If the current state is the terminal state, the program restarts and checks if it returns to state A.
- If the current state is not a valid state, the program breaks the loop.
- Visualizes the resulting state machine using Graphviz and saves the diagram to a file.
- Prints a message indicating the number of requests made and the file where the state machine diagram is saved.

## Conclusion
This program demonstrates how to use sockets and dictionaries in Python to build a state machine from data received over a network connection. The resulting state machine is visualized using Graphviz, making it easy to understand and analyze.