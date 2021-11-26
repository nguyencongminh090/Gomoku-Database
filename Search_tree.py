class Node:
    def __init__(self, node=None):
        self.child = []
        self.node = node
        self.depth = ''
        self.val = ''
        self.note = ''

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
        return 'Not found' if len(lst) != 0 and lst[0] not in child else self.child[child.index(lst[0])].get_move(lst[1:]) \
            if len(lst) != 0 else child if len(child) != 0 else 'Empty'

    def set_depth(self, lst: list, depth):
        child = [i.node for i in self.child]
        if len(lst) != 0 and lst[0] not in child:
            return 'Not found'
        elif len(lst) != 0 and lst[0] in child:
            return self.child[child.index(lst[0])].set_depth(lst[1:])
        elif len(lst) == 0:
            self.depth = str(depth)
        return

    def set_val(self, lst: list, val):
        child = [i.node for i in self.child]
        if len(lst) != 0 and lst[0] not in child:
            return 'Not found'
        elif len(lst) != 0 and lst[0] in child:
            return self.child[child.index(lst[0])].set_val(lst[1:])
        elif len(lst) == 0:
            self.val = str(val)
        return

    def set_note(self, lst: list, note):
        child = [i.node for i in self.child]
        if len(lst) != 0 and lst[0] not in child:
            return 'Not found'
        elif len(lst) != 0 and lst[0] in child:
            return self.child[child.index(lst[0])].set_note(lst[1:])
        elif len(lst) == 0:
            self.val = str(note)
        return

    def __str__(self, level=-1):
        ret = "    "*level+str(self.node)+"\n"
        for child in self.child:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node>'

tree = Node('Tree Node')
tree.add(['h3', 'e8', 'm5'])
tree.add(['h3', 'e8', 'm6'])
tree.add(['h3', 'm4', 'm5'])
tree.add(['k5', 'c3', 'l4'])
tree.add(['k5', 'c1', 'l4'])

print(str(tree))

