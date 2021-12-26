from time import perf_counter as clock
import time
import codecs
import win32api
import win32con
import os
import recognize_board


class Node:
    def __init__(self, node=None, root=False):
        self.child = []
        self.node = node
        self.root = root
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
        return 'Not found' if len(lst) != 0 and lst[0] not in child else \
            self.child[child.index(lst[0])].get_move(lst[1:]) \
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

    def total_nodes(self):
        if self.root:
            n = 0
        else:
            n = 1 
        for child in self.child:
            n += child.total_nodes()
        return n
    
    def click_on_screen(self, lag=0.0):
        control = Control(lag)
        if self.root:
            pass
        else:
            control.click(self.node)
        for child in self.child:
            child.click_on_screen(lag)
        control.undo()
        return

    def __str__(self, level=-1):
        ret = "    "*level+str(self.node)+"\n"
        for child in self.child:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node>'


class Control:
    def __init__(self, lag=0.0):
        if not os.path.exists('config.txt'):
            raise RuntimeError('No config found!')
        with open('config.txt') as f:
            self.dis = float(f.readline())
            self.x2, self.y2, self.x1, self.y1 = f.readline().split(' ')
        self.lag = lag

    def solve_coord(self, move):
        x = (round((ord(move[0]) - 97) * self.dis)) + int(self.x2)
        y = round((15 - int(move[1:])) * self.dis) + int(self.y2)
        return x, y

    def click(self, move):
        move = self.solve_coord(move)
        win32api.SetCursorPos((round(move[0]), round(move[1])))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        # lag
        time.sleep(self.lag)

    def undo(self):
        win32api.keybd_event(0x25, 0, 0, 0)
        win32api.keybd_event(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(self.lag)


def main():
    while True:
        db = input('Database name: ')
        if not os.path.exists(db):
            print('---File not found! Please Try Again!---'.center(70))
            continue
        print(f'\n{"-"*70}\nIntroduce\n-'
              f' q: Quit\n'
              f'- clear: Clear screen\n'
              f'- c: Change database\n'
              f'- export: Copy to Renlib\n'
              f'- total_node: Count total nodes in tree\n'
              f'- Help: Display help'
              f'Author: Nguyen Cong Minh\n{"-"*70}\n')
        with open(db, 'rb') as f:
            data = codecs.decode(f.read(), 'bz2').decode().split('\n')[:-1]
            
        tree = Node(root=True)
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
            elif ''.join(inp).upper() == 'EXPORT':
                recognize_board.recognize()
                print('NOTE:', "to let the program work probably, the time's lag should be 0.03 seconds")
                inp_lag = float(input('Lag (s): '))
                tree.click_on_screen(inp_lag)
                continue
            elif ''.join(inp).upper() == 'TOTAL_NODE':                
                print(f'{tree.total_nodes()} nodes in tree')
                continue
            elif ''.join(inp).upper() == 'HELP':
                print(f'\n{"-"*70}\nHelp\n'
                      f'- q: Quit\n'
                      f'- clear: Clear screen\n'
                      f'- c: Change database\n'
                      f'- export: Copy to Renlib\n'
                      f'- total_node: Count total nodes in tree\n'
                      f'- Help: Display help')
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
