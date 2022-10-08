import copy
import random

#jumaniespi
def is_winning(map, n):
    for j in range(0,7,3):
        if map[0+j] == n and map[1+j] == n and map[2+j] == n:
            return True
    for j in range(3):
        if map[0+j] == n and map[3+j] == n and map[6+j] == n:
            return True
    for j in range(0,3,2):
        if map[0+j] == n and map[4] == n and map[8-j] == n:
            return True

class State:
    def __init__(self, parent, child_id : int, player : int, deep : int):
        self.player = player
        self.deep = deep
        self.children = []
        self.value = [100, 100]
        self.selected_field = -1     
        if parent != None:
            self.fields = copy.deepcopy(parent.fields)
            self.parent = parent
            for i in range(len(self.fields)):
                if self.fields[i] == 0:
                    if child_id == 0:
                        self.fields[i] = player
                        self.selected_field = i
                        return
                    else:
                        child_id -= 1  
        else:            
            self.fields = [0, 0, 0,
                           0, 0, 0,
                           0, 0, 0]
            self.parent = None
    def create_child(self, n : int):
        return State(self, n, -self.player, self.deep + 1)
    def create_children(self):
        ret = []
        for i in range(0, 8 - self.deep):
            ret.append(self.create_child(i))
        return ret
    def create_next_states(self):
        if is_winning(self.fields, -1):
            return
        if is_winning(self.fields, 1):
            return
        if self.deep == 8:
            return
        self.children = self.create_children()
        for child in self.children:
            child.create_next_states()
    def calculate_value(self):
        if len(self.children) == 0:
            if is_winning(self.fields, -1):
                self.value[0] = 0
                self.value[1] = 100              
            elif is_winning(self.fields, 1):
                self.value[0] = 100               
                self.value[1] = 0          
            return [self.value[0], self.value[1]]
        losing_states = 0
        for child in self.children:
            value = child.calculate_value()
            self.value[0] = min(self.value[0], value[0])
            self.value[1] = min(self.value[1], value[1])
            if value[1] == 1:
                losing_states += 1
        self.value[0] += 1
        self.value[1] += 1
        if losing_states == len(self.children) and self.player == 1:
            self.value[1] = 0
        return [self.value[0], self.value[1]]
    def choose(self):
        max_value = 0
        for child in self.children:
            if child.value[0] == 0:
                return child.selected_field
            if child.value[1] >= max_value:
                max_value = child.value[1]
                best_option = child
        return best_option.selected_field
    
def debug_state(state : State):
    current = state
    while len(current.children) > 0:
        i = 0
        for ch in current.children:
            print(i, end = ' ')
            print(' = ', end = ' ')
            print(ch.fields, end = ' ')
            print(' : ', end = ' ')
            print(ch.value)
            i += 1
        print('best target field :', end = ' ')
        print(current.choose())
        select = input()
        current = current.children[int(select)]

def ai_debug():
    state = State(None, 0, 1, 0)
    state.create_next_states()
    state.calculate_value()
    debug_state(state)
    
def choose_first_move(fields):
    if fields[4] == 1:
        return random.choice([0, 2, 6, 8])
    return 4

        
def choice_ai_d(map, not_used):
    fields = []
    deep = 0
    for m in map:
        fields.append(m[1])
        if m[1] == -1 or m[1] == 1:
            deep += 1
    if deep == 1:
        chosen = choose_first_move(fields)
        return map[chosen][0]
    state = State(None, 0, 1, deep - 1)
    state.fields = fields
    state.create_next_states()
    state.calculate_value()
    best = state.choose()
    #print(best)
    #debug_state(state)
    return map[best][0]
    
    
def debug_choice_ai():
    data =[[0, 1], [0, 0], [0, 0], 
           [0, 0], [0, 1], [0, 0],
           [0, 0], [0, 0], [0, -1]]
    choice_ai_d(data, 0)
        
debug_choice_ai()
