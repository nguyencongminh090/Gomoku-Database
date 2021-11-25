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


tree = Node()
tree.add(['h3', 'e8', 'm5'])
tree.add(['h3', 'e8', 'm6'])
tree.add(['h3', 'm4', 'm5'])
tree.add(['k5', 'c3', 'l4'])
tree.add(['k5', 'c1', 'l4'])

print(tree.get_move(['h3', 'e8']))
print(tree.get_move(['k5']))
