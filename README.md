# App to determine the state machine structure
This program connects to a server and requests data to identify the structure of a state machine that was created randomly. The state machine is stored as a dictionary with keys representing states and values representing transitions. The program determines the structure of the state machine and generates a visual representation using Graphviz.

## Requirements
- Python 3.x
- Graphviz

## Installation
1. Clone the repository: git clone https://github.com/vishnu123r/State_machine_MEQ.git
2. Install the required packages: pip install -r requirements.txt
3. Install Graphviz 8.0.1 (https://graphviz.org/download/) and add it to the PATH environment variable

## Usage
1. Open a terminal and navigate to the directory where the program is located.
2. Run the program: python app.py
3. Wait for the program to finish running.
4. The structure of the state machine will open as a PDF file.
5. The resulting state machine diagram will be saved to the state_machine_{timestamp}.gv file in the "img" directory.

## Functionality
The program does the following:
- Imports necessary libraries and functions.
- Initializes constants and creates the initial state machine dictionary.
- Connects to the server using a socket and receives the initial state.
- Loops while the number of keys in the state machine dicitonary is less than the maximum number of possible keys.
- Uses one of two request strategies to send a request to the server and receive a response.
- Adds the new transition to the state machine dictionary.
- Updates the current state based on the response.
- If the current state is the terminal state, the state returns to A.
- If the current state is not a valid state, error is raised.
- Prints a message indicating the number of requests made and the file where the state machine diagram is saved.
- Prints the state machine structure dictionary
- Visualizes the resulting state machine using Graphviz and saves the diagram to a file.

## Expected results
![Expected results](img\Screenshot 2023-04-12_161957.png)

## Conclusion
This program demonstrates how to use sockets and dictionaries in Python to determine the state machine structure from data received over a network connection. The resulting state machine is visualized using Graphviz, making it easy to understand and analyze.
