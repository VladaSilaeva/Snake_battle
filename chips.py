class Chip:
    CELL_TYPES = {'my_tail': 'x', 'my_body': '-', 'my_head': 'o',
                  'other_tail': '*', 'other_body': '=', 'other_head': 'q',
                  'empty': ' ', 'wall': '#', None: '.'}
    DEFAULT_BOARD = [[None] * 7 for _ in range(7)]
    DEFAULT_BOARD[3][3] = 'my_head'

    def __init__(self, board=None, groups_or=None, groups_and=None, groups_ex=None):
        if board is None or len(board) != 7:
            board = Chip.DEFAULT_BOARD
        self.board = board
        self.groups_and = {'': [], 'and1': [], 'and2': []}
        self.groups_or = {'or1': [], 'or2': []}
        self.groups_ex = {'ex1': [], 'ex2': []}
        if groups_and is not None:
            for key in self.groups_and:
                if key in groups_and:
                    self.groups_and[key] = list(groups_and[key])
        if groups_or is not None:
            for key in self.groups_or:
                if key in groups_or:
                    self.groups_or[key] = list(groups_or[key])
        if groups_ex is not None:
            for key in self.groups_ex:
                if key in groups_ex:
                    self.groups_ex[key] = list(groups_ex[key])

    def edit(self, h, w, cell_type, group='', *args):
        if 0 <= h < 7 and 0 <= w < 7 and cell_type in Chip.CELL_TYPES.keys() \
                and group in list(self.groups_and.keys()) + list(self.groups_or.keys()) +\
                list(self.groups_ex.keys()) and not len(args):
            if cell_type == 'my_head':
                print('--fail--')
                return
            self.board[h][w] = cell_type
            for g in self.groups_and.keys():
                if (h, w) in self.groups_and[g]:
                    del self.groups_and[g][self.groups_and[g].index((h, w))]
            for g in self.groups_or.keys():
                if (h, w) in self.groups_or[g]:
                    del self.groups_and[g][self.groups_or[g].index((h, w))]
            for g in self.groups_ex.keys():
                if (h, w) in self.groups_ex[g]:
                    del self.groups_and[g][self.groups_ex[g].index((h, w))]
            if group == '':
                self.groups_and[group].append((h, w))
            elif 'and' in group:
                self.groups_and[group].append((h, w))
            elif 'or' in group:
                self.groups_or[group].append((h, w))
            else:
                self.groups_ex[group].append((h, w))
        else:
            print('--fail--')

    def print(self, with_groups=False):
        for row in self.board:
            for cell in row:
                print(Chip.CELL_TYPES[cell], end=' ')
            print()
        if with_groups:
            for g in self.groups_and.keys():
                print(f'{g}: {self.groups_and[g]}')
            for g in self.groups_or.keys():
                print(f'{g}: {self.groups_or[g]}')
            for g in self.groups_ex.keys():
                print(f'{g}: {self.groups_ex[g]}')

    def reversed(self):
        return Chip([row[::-1] for row in self.board])
