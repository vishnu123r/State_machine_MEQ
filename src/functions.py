from graphviz import Digraph

def count_key_dict(dct):
    "This returns the number of keys in a dicitonary"
    count = len(dct)
    for key, value in dct.items():
        if isinstance(value, dict):
            count += count_key_dict(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    count += count_key_dict(item)
    return count

def state_machine_viz(state_machine):
    graph = Digraph()
    graph.attr(rankdir='LR')

    
    state_list = list(state_machine.keys())
    for state in state_list:
        graph.node(state)
    
    for start_state in state_machine:
        transition_dict = state_machine[start_state]
        for action in ['1', '2', '3']:
            end_state = transition_dict[action]
            graph.edge(start_state, end_state, label=action)
    
    graph.render('state_machine.gv', view=True)



if __name__ == "__main__":
        
    #Create a state machine dictionary
    state_machine = {
        "A": {"1": "B", "2": "C", "3": "D"},
        "B": {"1": "E", "2": "F", "3": "G"},
        "C": {"1": "H", "2": "I", "3": "J"},
        "D": {"1": "K", "2": "L", "3": "M"},
        "E": {"1": "N", "2": "O", "3": "P"},
        "F": {"1": "Q", "2": "R", "3": "S"},
        "G": {"1": "T", "2": "U", "3": "V"},
        "H": {"1": "W", "2": "X", "3": "Y"},
        "I": {"1": "Z", "2": "A", "3": "B"},
        "J": {"1": "C", "2": "D", "3": "E"},
        "K": {"1": "F", "2": "G", "3": "H"},
        "L": {"1": "I", "2": "J", "3": "K"},
        "M": {"1": "L", "2": "M", "3": "N"},
        "N": {"1": "O", "2": "P", "3": "Q"},
        "O": {"1": "R", "2": "S", "3": "T"},
        "P": {"1": "U", "2": "V", "3": "W"},
        "Q": {"1": "X", "2": "Y", "3": "Z"},
        "R": {"1": "A", "2": "B", "3": "C"},
        "S": {"1": "D", "2": "E", "3": "F"},
        "T": {"1": "G", "2": "H", "3": "I"},
        "U": {"1": "J", "2": "K", "3": "L"},
        "V": {"1": "M", "2": "N", "3": "O"},
        "W": {"1": "P", "2": "Q", "3": "R"},
        "X": {"1": "S", "2": "T", "3": "U"},
        "Y": {"1": "V", "2": "W", "3": "X"},
        "Z": {"1": "Y", "2": "Z", "3": "A"}
    }


    state_machine_viz(state_machine)
        
