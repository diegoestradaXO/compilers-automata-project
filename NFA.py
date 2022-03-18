from email.quoprimime import body_encode
from operator import truediv
from Node import Node
from re import search
from regex import *


class NFA():
    def __init__(self, regex):
        self.start_state = None
        self.final_state = None
        self.states = []
        self.symbols = []
        self.ids = 0
        print(regex)
        self.process_regex(regex)

        
    # Verifies if a given character belongs to the valid symbols (letters, numbers and epsilon)
    def is_char_symbol(self, character):
        symbols = 'abcdefghijklmnopqrstuvwxyz0123456789' + 'ε'
        return symbols.find(character) != -1


    # postfix evaluation of symbols and operators
    def process_regex(self, expresion):
        symbols_stack = []
        ops = []
        i = 0
        while i < len(expresion):
            if expresion[i] == '(':
                ops.append(expresion[i])

            elif self.is_char_symbol(expresion[i]): # Symbol
                
                chars = ''
                while i < len(expresion) and self.is_char_symbol(expresion[i]): # is the char a valid symbol?
                    chars += expresion[i] # if is valid, add it to the val string
                    i += 1 # keep iterating the next elements after the symbol found

                symbols_stack.append(chars)
                i -= 1

            elif expresion[i] == ')':
                while len(ops) != 0 and ops[-1] != '(': # verifies that there are more ops and that the last op is not open parenthesis
                    op = ops.pop() # obtains last operator 
                    chars2 = symbols_stack.pop() #obtains last symbol
                    chars1 = None # opens posibility for second symbol

                    if op != '*' and op != '+' and op != '?': 
                        chars1 = symbols_stack.pop() # in case it is concat or |
                    
                    start, end = self.create_operation(chars1, chars2, op) # proceeds to create operation between two symbols, or it could be just one, depending in the last if statement
                    symbols_stack.append((start, end))

                ops.pop()

            else:
                while (len(ops) != 0 and self.get_precedence(ops[-1]) >= self.get_precedence(expresion[i])):
                    op = ops.pop()
                    chars2 = symbols_stack.pop()
                    chars1 = None

                    if op != '*' and op != '+' and op != '?':
                        chars1 = symbols_stack.pop()
                    
                    start, end = self.create_operation(chars1, chars2, op)
                    symbols_stack.append((start, end))
                ops.append(expresion[i])

            i += 1

        while len(ops) != 0:
            op = ops.pop()
            chars2 = symbols_stack.pop()
            chars1 = None

            if op != '*' and op != '+' and op != '?':
                chars1 = symbols_stack.pop()
            
            start, end = self.create_operation(chars1, chars2, op)
            symbols_stack.append((start, end))
        
        self.start_state, self.final_state = symbols_stack.pop()

    # Creates states and nodes using the operation identities
    def create_operation(self, x, y, operator):
        if operator == '|':
            return self.or_identity(x,y)
        if operator == '.': 
            return self.concat_identity(x, y)
        if operator == '*': 
            return self.kleene_identity(y)

    def or_identity(self, a, b):
        #          (a)---------->(b)
        #         /                 \
        #        /                   \
        # start-                       >final
        #        \                   /
        #         \                 /
        #          (c)---------->(d)

        if type(a) == tuple and type(b) == tuple:
            start_a, end_a = [*a]
            start_b, end_b = [*b]
            end_node = Node(self.ids + 2, [])
            start_node = Node(self.ids + 1, [('ε', start_a), ('ε', start_b)])
            end_a.AddTransition('ε', end_node)
            end_b.AddTransition('ε', end_node)
            self.ids += 2
            self.states.append(end_node)
            self.states.append(start_node)
            return start_node, end_node
            
        elif type(a) != tuple and type(b) != tuple:
            end_node = Node(self.ids + 6, [])
            end_a_node = Node(self.ids + 5, [('ε', end_node)])
            end_b_node = Node(self.ids + 4, [('ε', end_node)])
            start_a_node = Node(self.ids + 3, [(a, end_a_node)])
            start_b_node = Node(self.ids + 2, [(b, end_b_node)])
            start_node = Node(self.ids + 1, [('ε', start_a_node), ('ε', start_b_node)])
            self.ids += 6
            self.states.append(end_node)
            self.states.append(end_a_node)
            self.states.append(end_b_node)
            self.states.append(start_a_node)
            self.states.append(start_b_node)
            self.states.append(start_node)
            return start_node, end_node
        elif type(a) != tuple and type(b) == tuple:
            start_b, end_b = [*b]
            end_node = Node(self.ids + 4, [])
            end_a_node = Node(self.ids + 3, [('ε', end_node)])
            start_a_node = Node(self.ids + 2, [(a, end_a_node)])
            start_node = Node(self.ids + 1, [('ε', start_b), ('ε', start_a_node)])
            end_b.AddTransition('ε', end_node)
            self.ids += 4
            self.states.append(end_node)
            self.states.append(end_a_node)
            self.states.append(start_a_node)
            self.states.append(start_node)
            return start_node, end_node
        elif type(a) == tuple and type(b) != tuple:
            start_a, end_a = [*a]
            end_node = Node(self.ids + 4, [])
            end_b_node = Node(self.ids + 3, [('ε', end_node)])
            start_b_node = Node(self.ids + 2, [(b, end_b_node)])
            start_node = Node(self.ids + 1, [('ε', start_a), ('ε', start_b_node)])
            end_a.AddTransition('ε', end_node)
            self.ids += 4
            self.states.append(end_node)
            self.states.append(end_b_node)
            self.states.append(start_b_node)
            self.states.append(start_node)
            return start_node, end_node  

    def concat_identity(self, a, b):
        #
        #
        # start ----->(a)--------->(b)-------> end
        #
        #

        if type(a) == tuple and type(b) == tuple:
            start_a, end_a = [*a]
            start_b, end_b = [*b]
            self.merge_nodes(end_a, start_b)
            return start_a, end_b
        elif type(a) != tuple and type(b) != tuple:
            b_node = Node(self.ids + 3, [])
            a_node = Node(self.ids + 2, [(b, b_node)])
            start_node = Node(self.ids + 1, [(a, a_node)])
            self.ids += 3
            self.states.append(start_node)
            self.states.append(a_node)
            self.states.append(b_node)            
            return start_node, b_node
        elif type(a) != tuple and type(b) == tuple:
            start_b, end_b = [*b]
            start_node = Node(self.ids + 1, [(a, start_b)])
            self.states.append(start_node)
            self.ids += 1
            return start_node, end_b
        elif type(a) == tuple and type(b) != tuple:
            start_a, end_a = [*a]
            end_node = Node(self.ids + 1, [])
            self.states.append(end_node)
            end_a.AddTransition(b, end_node)
            self.ids += 1
            return start_a, end_node

    def kleene_identity(self, a, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        #                _________
        #              </         \
        # start ----->(a)--------->(b)-------> end
        #     \______________________________/>
        #

        if type(a) == tuple:
            start_a, end_a = [*a]
            end_node = Node(self.ids + 2, [])
            start_node = Node(self.ids + 1, [('ε', start_a), ('ε', end_node)])
            end_a.AddTransition('ε', end_node)
            end_a.AddTransition('ε', start_a)
            self.ids += 2
            self.states.append(start_node)
            self.states.append(end_node)
            return start_node, end_node
        else:
            end_node = Node(self.ids + 4, [])
            node3 = Node(self.ids + 3, [('ε', end_node)])
            node2 = Node(self.ids + 2, [(a, node3)])
            start_node = Node(self.ids + 1, [('ε', node2), ('ε', end_node)])
            node3.AddTransition('ε', node2)
            self.ids += 4
            self.states.append(start_node)
            self.states.append(node2)
            self.states.append(node3)
            self.states.append(end_node)
            return start_node, end_node

    def simulate_string(self, exp):
        S = self.epsilon_closure([self.start_state])

        for e in exp:
            S = self.epsilon_closure(self.make_transition(S, e))

        my_states = []
        for i in S:
            my_states.append(str(i.id))
        
        my_final_state = str(self.final_state.id)
        if my_final_state in my_states:
            return 'YES'
        else:
            return 'NO'

    def is_node_in_states(self, states, n):
        my_states = []
        for i in states:
            my_states.append(str(i.id))
        
        if str(n.id) in my_states:
            return True
        else:
            return False

    def epsilon_closure(self, states):
        stack = [] + states
        closure = [] + states

        while len(stack) != 0:
            t = stack.pop()

            for transition in t.transitions:
                s, state = [*transition]
                if 'ε' == s:
                    if not self.is_node_in_states(closure, state):
                        stack.append(state)
                        closure.append(state)

        return closure

    def make_transition(self, T, symbol):
        moves = []
        for t in T:
            for transition in t.transitions:
                s, state = [*transition]
                if symbol == s:
                    moves.append(state)

        return moves

    def get_states(self):
        return {str(s.id) for s in self.states}

    def make_trans_function(self):
        function = {}
        for i in self.states:
            cont = 1
            function[str(i.id)] = {}

            for j in i.transitions:
                symbol, node = [*j]

                if str(symbol) in function[str(i.id)].keys():
                    function[str(i.id)][str(symbol) + ' '*cont] = str(node.id)
                    cont += 1
                else:
                    function[str(i.id)][str(symbol)] = str(node.id)
        return function
        
    def merge_nodes(self, nodeA, nodeB):
        # Quitar de estados
        nodeA.transitions += nodeB.transitions
        i = self.states.index(nodeB)
        self.states.pop(i)

    def get_precedence(self, operator):
        if operator == '|':
            return 1
        if operator == '.':
            return 2
        if operator == '*' or operator == '+' or operator == '?':
            return 3
        return 0