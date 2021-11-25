from time import perf_counter as clock


class Node:
    def __init__(self, node=None):
        self.child = []
        self.node = node

    def add(self, lst: list):
        child = [i.node for i in self.child]
        if lst[0] not in child:
            self.child.append(Node(lst[0]))
        self.insert(lst)

    def insert(self, lst: list, it=1):
        if len(lst) >= 2:
            child = [i.node for i in self.child]
            if lst[it - 1] in child:
                return self.child[child.index(lst[it - 1])].insert(lst, it)                
            if lst[it] not in child:
                self.child.append(Node(lst[it]))
            self.insert(lst[1:])
        return

    def get_move(self, lst: list):
        child = [i.node for i in self.child]
        return self.child[child.index(lst[0])].get_move(lst[1:]) \
            if len(lst) != 0 else child if len(child) > 1 else child[0]


with open('EVA.txt', 'r') as f:
    data = f.read().split('\n')[:-1]

tree = Node()
for i in range(len(data)):
    tree.add(data[i].split(' '))

while True:
    inp = input('Search: ').split(' ')
    while '' in inp:
        inp.remove('')
    try:
        a = clock()
        move = tree.get_move(inp)
        b = clock()
        print('Variants:', move)
        print('Runtime: %.9f' % (b-a))
    except:
        print('Not found')
    if ''.join(inp).upper() == 'Q':
        break
