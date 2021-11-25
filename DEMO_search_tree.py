from time import perf_counter as clock
import codecs
import os


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
        return 'Not found' if len(lst) != 0 and lst[0] not in child else self.child[child.index(lst[0])].get_move(lst[1:]) \
            if len(lst) != 0 else child


def main():
    while True:
        db = input('Database name: ')
        if not os.path.exists(db):
            print('---File not found! Please Try Again!---'.center(70))
            continue
        print(f'\n{"-"*70}\nIntroduce\n- q: Quit\n- clear: Clear screen\n- c: Change database\nAuthor: Nguyen Cong Minh\n{"-"*70}\n')
        with open(db, 'rb') as f:
            data = codecs.decode(f.read(), 'bz2').decode().split('\n')[:-1]
            
        tree = Node()
        for i in range(len(data)):
            tree.add(data[i].split(' '))

        while True:
            inp = input('Input: ').split(' ')
            
            while '' in inp:
                inp.remove('')
                
            if ''.join(inp).upper() == 'Q':
                exit()
            elif ''.join(inp).upper() == 'C':
                os.system('cls')
                break
            elif ''.join(inp).upper() == 'CLEAR':
                os.system('cls')
                continue
                
            a = clock()
            move = tree.get_move(inp)
            b = clock()
            
            print(f'Search <{" ".join(inp)}> in database')
            print('--*-> Variants:')
            if move != 'Not found':
                for i in move:
                    print(f'[+] {i}')
                print(f'\n{"~"*30}\nRuntime: %.9f sec\n{"~"*30}\n' % (b-a))
            else:
                print('--x->', move)
            
            
    return


if __name__ == '__main__':
    main()
