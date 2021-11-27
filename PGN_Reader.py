import codecs


class PGN:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path + '.txt') as f:
            text = f.read().split('\n')
        return text[:-2]

    def split_pgn(self):
        text = self.read()
        out = []
        stack = []
        c = False
        for i in range(len(text)):
            if text[i] == '':
                continue
            if (('0-1' in text[i]) or ('1-1' in text[i]) or ('1-0' in text[i]) or ('1/2' in text[i])) and c == True:
                stack.append(text[i].strip('\n'))
                out.append('\n'.join(stack[:12]) + '\n' + ' '.join(stack[12:]))
                stack.clear()
                c = False
            else:
                stack.append(text[i].strip('\n'))
                if ('0-1' in text[i]) or ('1-1' in text[i]) or ('1-0' in text[i]):
                    c = True        
        return out

    @staticmethod
    def check_winner(pgn, pn):
        '''
        pgn: PGN game
        pn: Player name
        '''
        pgn = pgn.split('\n')
        bp = pgn[4][8:-2]
        wp = pgn[5][8:-2]
        re = pgn[6][9:-2].split('-')
##        print('Black:', bp)
##        print('White:', wp)
##        print('Result:', re)
        return [bp, wp][re.index('1')] == pn if '1' in re else False

    @staticmethod
    def get_move(pgn):
        '''
        pgn: PGN game
        '''
        pgn = pgn.split('\n')
        return pgn[-1]

    @staticmethod
    def reformat_move(arr):
        def chk(string):
            num = []
            for i in string:
                if i.isnumeric():
                    num.append(i)
            num = ''.join(num)
            tmp = string.replace(num, '*')
            tmp = tmp.replace('.', '*')
            tmp = tmp.replace('*', '')
            if tmp != '':
                return False
            else:
                return True
            
        tmk = arr.split(' ')
        for i in range(len(tmk)):
            if chk(tmk[i]) == True:
                tmk.remove(tmk[i])
                tmk.insert(i,'*')
            elif (tmk[i] == 'black') or (tmk[i] == 'white') or (tmk[i] == '--') or (tmk[i] == '0-1') or (tmk[i] == '1-0') or (tmk[i] == '1/2-1/2'):
                tmk.remove(tmk[i])
                tmk.insert(i, '*')
        tmk = ' '.join(tmk)
        tmk = tmk.replace('* ', '')
        tmk = tmk.replace('*', '')  
        tmk = tmk.split(' ')
        while '' in tmk:
            tmk.remove('')
        return tmk

def make_db(fn, search_game_of, file_out):
    pgn = PGN(fn)
    game = pgn.split_pgn()
    s = ''
    with open(file_out, 'wb') as f:
        for i in game:
            if pgn.check_winner(i, search_game_of):
                move = ' '.join(pgn.reformat_move(pgn.get_move(i)))
                s += move + '\n'
        s = codecs.encode(bytes(s.encode()), 'bz2')
        f.write(s)
    return


if __name__ == '__main__':
    make_db('runglathap', 'runglathap', 'runglathap.db')
