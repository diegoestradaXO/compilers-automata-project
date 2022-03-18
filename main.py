from sympy import false, true
from NFA import NFA
from Node import Node
import utils
from regex import *

flag = true
while flag:
    print("Hello user! This software was made for converting a regular expresion to NFA and DFA")
    print("Please select an option from the menu below...")
    print("\n")
    print("1. Regex to NFA (Thompson)")
    print("2. Regex to DFA (Subsets)")
    print("3. Exit")
    print("\n")

    users_choice = int(input(">> "))
    if users_choice == 1:
        print(">> Please write down your regular expresion:")
        exp = input('>> ')
        print(">> Write a string to verify:")
        w = input('>> ')
        # try:
        my_regex = fix_regex(exp)
        nfa = NFA(my_regex)
        alphabet, alphabet_print = utils.get_alphabet(nfa.make_trans_function())
        respuesta = nfa.simulate_string(w)
        print(f'Is {w} accepted in {exp}? -> ', respuesta)
        utils.graph_fa(nfa.get_states(), alphabet, str(nfa.start_state.id), {str(nfa.final_state.id)}, nfa.make_trans_function(), 'graphs/nfa')
        
        # except:
        #     print('An error ocurred with the creation of the nfa with thompson algorithm')
    elif users_choice == 2:
        pass
    elif users_choice == 3:
        flag = False



