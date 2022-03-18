class Node():
    def __init__(self, identifier, transitions = []):
        self.id = identifier
        self.transitions = transitions

    def AddTransition(self, symbol, state):
        self.transitions.append((symbol, state))
