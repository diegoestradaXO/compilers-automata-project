from sympy import false, true
from NFA import NFA
from DFA import DFA
import utils
from regex import *
import time

flag = true
while flag:
    print("\nHello user! This software was made for converting a regular expresion to NFA and DFA")
    print("Please select an option from the menu below...")
    print("\n")
    print("1. Regex to NFA (Thompson)")
    print("2. Regex to DFA (Direct)")
    print("3. Exit")
    print("\n")
    users_choice = int(input(">> "))
    if users_choice == 1:
        try:

            print("\n>> Please write down your regular expresion:")
            exp = input('>> ')
            print("\n>> Write a string to verify:")
            w = input('>> ')

            my_regex = fix_regex(exp)
            nfa = NFA(my_regex)
            alphabet, alphabet_print = utils.get_alphabet(nfa.make_trans_function())
            print(alphabet_print)
            start = time.time()
            respuesta = nfa.simulate_string(w)
            end = time.time()
            print(f'\nIs {w} accepted in {exp}? -> ', respuesta)
            print('time elapsed :', end - start, "seconds")
            utils.graph_fa(nfa.get_states(), alphabet, str(nfa.start_state.id), {str(nfa.final_state.id)}, nfa.make_trans_function(), 'graphs/nfa')
        except:
            print("An error ocurred while building the NFA... \n") 


    elif users_choice == 2:
        print("\n>> Please write down your regular expresion:")
        exp = input('>> ')
        print("\n>> Write a string to verify:")
        w = input('>> ')

        my_regex = fix_regex(exp, True)
        syntax = DFA(my_regex)

        states = {s.name for s in syntax.states}
        initial_state = syntax.init_state
        accepting_state = {s for s in syntax.acc_states}
        alphabet = {a for a in syntax.symbols}
        transition_function = syntax.create_transitions()
        alphabet, alphabet_print = utils.get_alphabet(transition_function)

        
        respuesta = syntax.simulate_string(w)

        print(f'\nIs {w} accepted in {exp}? -> ', respuesta)
        utils.graph_fa(states, alphabet, initial_state, accepting_state, transition_function, 'graphs/DIRECT_AFD')
    
    elif users_choice == 3:
        flag = False





