class Chip:
    def __init__(self):
        self.field = [['.'] * 7 for _ in range(7)]
        self.field[3][3] = 'my_head'
        self.groups = {'and0': [], 'and1': [], 'and2': [], 'and3': [], 'or1': [], 'or2': []}
        self.cell_types = {'my_tail': 'x', 'my_body': '-', 'my_head': 'o',
                           'other_tail': '*', 'other_body': '=', 'other_head': 'q',
                           'empty': ' ', 'wall': '#', '': '.'}

    def add(self, h, w, cell_type, group='and0', *args):
        h, w = int(h), int(w)
        if 0 <= h < 7 and 0 <= w < 7 and cell_type in self.cell_types.keys() \
                and group in self.groups.keys() and not len(args):
            if cell_type == 'my_head':
                print('--fail--')
                return
                # for i in range(len(self.field)):
                #     if 'o' in self.field[i]:
                #         self.field[i][self.field[i].index('o')] = '.'
                #         break
            self.field[h][w] = self.cell_types[cell_type]
            for g in self.groups.keys():
                if (h, w) in self.groups[g]:
                    del self.groups[g][self.groups[g].index((h, w))]
            self.groups[group].append((h, w))
        else:
            print('--fail--')

    def print(self, with_groups=False):
        for row in self.field:
            for cell in row:
                print(self.cell_types[cell], end=' ')
            print()
        if with_groups:
            for g in self.groups.keys():
                print(f'{g}: {self.groups[g]}')


text = '''Напиши координаты (два числа от 0 до 6 через пробел).
Затем через пробел напиши тип клетки (my/other tail/body/head или empty или wall).
Через пробел напиши группу (and1, and2, and3, or1, or2). Если клетка не состоит ни в какой из групп, не пиши ничего.'''
print(text)
ch = Chip()
answer = input()
while answer != 'конец':
    ch.add(*answer.split())
    answer = input()
ch.print(True)
