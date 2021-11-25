import os
from colorama import init, Fore, Style
from time import perf_counter as clock


init()

def search(inp, db):
    move = []
    for i in db:
        try:
            if False not in [i[j] == inp[j] for j in range(len(inp))]:
                if i[len(inp)] not in move:
                    move.append(i[len(inp)])
            else:
                continue
        except:
            continue
    return move


def main():
    f = open('EVA.txt', 'r')
    db = f.read().split('\n')
    f.close()
    db = [i.split(' ') for i in db]
    while True:
        move = []
        inp = input('--> Input move: ')
        if inp == 'quit':
            break
        elif inp == 'clear':
            os.system('cls')
        inp = inp.split(' ')
        while '' in inp:
            inp.remove('')
        a = clock()
        move = search(inp, db)
        b = clock()
        print('Runtime: %.9f' % (b - a))
        print('Variants:', move)

    pass


if __name__ == '__main__':
    main()
