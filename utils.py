from pythomata import SimpleDFA

def get_alphabet(transition):
    alphabet = []
    for v in transition.values():
        for k in v.keys():
            alphabet.append(k)

    return { *alphabet }, { *[a.replace(' ', '') for a in alphabet] }

def graph_fa(states, alphabet, initial_state, accepting_states, transition_function, name):
    fa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)
    graph = fa.to_graphviz()
    graph.render(name)
