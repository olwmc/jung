class CallStack:
    def __init__(self):
        self.call_stack = [0]

    def push(self, ix):
        self.call_stack.append(ix)

    def pop(self):
        self.call_stack.pop()
        
    def pointer(self):
        return self.call_stack[-1]

    def next(self):
        self.call_stack[-1] += 1

    def goto(self, location):
        if len(self.call_stack) == 0:
            self.call_stack.push(location)
        else:
            self.call_stack[-1] = location

class SymTab:
    def __init__(self):
        self.tab_stack = [{}]
        self.cur_tab = self.tab_stack[-1]

    def push(self, copy=False):
        if copy:
            self.tab_stack.append(self.tab_stack[-1].copy())
        else:
            self.tab_stack.append({})

    def pop(self):
        self.tab_stack.pop()

    def update(self, name, value):
        for tab in self.tab_stack[::-1]:
            if name in tab:
                tab[name] = value
                return
        self.tab_stack[-1][name] = value

    def get(self, name):
        for tab in self.tab_stack[::-1]:
            if name in tab:
                return tab[name]
        else:
            return 0

class State:
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        self.program = []
        self.label_table = dict()
        self.symbol_table = SymTab()
        self.call_stack = CallStack()
        self.stack = []

state = State()
