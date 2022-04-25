class Leaf():
    def __init__(self, name, position, is_operator, children, nullable):
        self.name = name
        self.position = position
        self.is_operator = is_operator
        self.children = children
        self.nullable = nullable
        self.first_pos = []
        self.last_pos = []
        self.follow_pos = []
        if self.name == 'ε':
            self.nullable = True
        self.AddFirstPos()
        self.AddLastPos()


    def GetName(self):
        name = f'{self.name} - {self.position}'
        return name

    def AddFirstPos(self):
        if self.is_operator:
            if self.name == '|':
                self.first_pos = self.children[0].first_pos + self.children[1].first_pos
            elif self.name == '.':
                if self.children[0].nullable:
                    self.first_pos = self.children[0].first_pos + self.children[1].first_pos
                else:
                    self.first_pos += self.children[0].first_pos
            elif self.name == '*':
                self.first_pos += self.children[0].first_pos
        else:
            if self.name != 'ε':
                self.first_pos.append(self.position)

    def AddLastPos(self):
        if self.is_operator:
            if self.name == '|':
                self.last_pos = self.children[0].last_pos + self.children[1].last_pos
            elif self.name == '.':
                if self.children[1].nullable:
                    self.last_pos = self.children[0].last_pos + self.children[1].last_pos
                else:
                    self.last_pos += self.children[1].last_pos
            elif self.name == '*':
                self.last_pos += self.children[0].last_pos
        else:
            if self.name != 'ε':
                self.last_pos.append(self.position)
