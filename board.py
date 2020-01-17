from random import choice, randint
import pygame


class Board:
    N_SNAKES = 4
    START_LEN_SNAKE = 10
    # LEN_VIEW = 7
    K = 3
    CELL_TYPES = {'wall4': '##', 'empty4': '__',
                  'head0': 'O0', 'body0': '=0', 'tail0': '-0',
                  'head1': 'O1', 'body1': '=1', 'tail1': '-1',
                  'head2': 'O2', 'body2': '=2', 'tail2': '-2',
                  'head3': 'O3', 'body3': '=3', 'tail3': '-3'}

    CELL_COLORS = {'wall4': (0, 0, 0), 'empty4': (200, 200, 200),
                   'head0': (255, 0, 0), 'body0': (255, 0, 0), 'tail0': (255, 0, 0),
                   'head1': (102, 255, 0), 'body1': (102, 255, 0), 'tail1': (102, 255, 0),
                   'head2': (255, 204, 0), 'body2': (255, 204, 0), 'tail2': (255, 204, 0),
                   'head3': (0, 0, 179), 'body3': (0, 0, 179), 'tail3': (0, 0, 179)}
    COLOR_BORDER = (255, 255, 255)

    def __init__(self, snakes_chips, screen, n):
        self.width = self.height = n
        self.screen = screen
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.board = [['empty4'] * (self.width + 2 * Board.K) for _ in range(self.width + 2 * Board.K)]
        self.len_board = len(self.board)
        for i in range(Board.K):
            self.board[i] = ['wall4'] * (self.width + 2 * Board.K)
            self.board[self.len_board - 1 - i] = ['wall4'] * (self.width + 2 * Board.K)
        for i in range(Board.K, self.width + Board.K):
            for j in range(Board.K):
                self.board[i][j] = 'wall4'
                self.board[i][self.len_board - 1 - j] = 'wall4'

        self.snakes_chips = snakes_chips
        self.snakes = [[(i + Board.K, self.len_board // 2
                         ) for i in range(Board.START_LEN_SNAKE - 1, -1, -1)] * bool(len(snakes_chips[0])),
                       [(self.len_board // 2, i + Board.K
                         ) for i in range(Board.START_LEN_SNAKE - 1, -1, -1)] * bool(len(snakes_chips[1])),
                       [(i - Board.K, self.len_board // 2
                         ) for i in range(self.len_board - Board.START_LEN_SNAKE, self.len_board
                                          )] * bool(len(snakes_chips[2])),
                       [(self.len_board // 2, i - Board.K
                         ) for i in range(self.len_board - Board.START_LEN_SNAKE, self.len_board
                                          )] * bool(len(snakes_chips[3]))]
        # print(*self.snakes, sep='\n')
        for i in range(Board.N_SNAKES):
            if len(self.snakes[i]):
                self.board[self.snakes[i][0][0]][self.snakes[i][0][1]] = 'head' + str(i)
                self.board[self.snakes[i][-1][0]][self.snakes[i][-1][1]] = 'tail' + str(i)
                for x, y in self.snakes[i][1:-1]:
                    self.board[x][y] = 'body' + str(i)

    def step(self):
        snakes_alive = 0
        snakes_can_move = 0
        for i in range(Board.N_SNAKES):
            # print(i)
            if len(self.snakes[i]) > 1:
                snakes_alive += 1
                snake_move = None
                snake_moves = []

                if self.board[self.snakes[i][0][0]][self.snakes[i][0][1] - 1] in ('empty4', 'tail0', 'tail1',
                                                                                  'tail2', 'tail3'):
                    if self.board[self.snakes[i][0][0]][self.snakes[i][0][1] - 1] != 'tail' + str(i):
                        snake_moves.append((self.snakes[i][0][0], self.snakes[i][0][1] - 1))
                if self.board[self.snakes[i][0][0] - 1][self.snakes[i][0][1]] in ('empty4', 'tail0', 'tail1',
                                                                                  'tail2', 'tail3'):
                    if self.board[self.snakes[i][0][0] - 1][self.snakes[i][0][1]] != 'tail' + str(i):
                        snake_moves.append((self.snakes[i][0][0] - 1, self.snakes[i][0][1]))
                if self.board[self.snakes[i][0][0] + 1][self.snakes[i][0][1]] in ('empty4', 'tail0', 'tail1',
                                                                                  'tail2', 'tail3'):
                    if self.board[self.snakes[i][0][0] + 1][self.snakes[i][0][1]] != 'tail' + str(i):
                        snake_moves.append((self.snakes[i][0][0] + 1, self.snakes[i][0][1]))
                if self.board[self.snakes[i][0][0]][self.snakes[i][0][1] + 1] in ('empty4', 'tail0', 'tail1',
                                                                                  'tail2', 'tail3'):
                    if self.board[self.snakes[i][0][0]][self.snakes[i][0][1] + 1] != 'tail' + str(i):
                        if len(snake_moves) == 0 or not randint(0, 2):
                            snake_moves.append((self.snakes[i][0][0], self.snakes[i][0][1] + 1))
                view0 = [self.board[j][self.snakes[i][0][1] - Board.K:self.snakes[i][0][1] + Board.K]
                         for j in range(self.snakes[i][0][0] - Board.K, self.snakes[i][0][0] + Board.K)]
                for k in range(len(view0)):
                    for m in range(len(view0[k])):
                        if int(view0[k][m][-1]) == 4:
                            view0[k][m] = view0[k][m][:-1]
                        elif int(view0[k][m][-1]) == i:
                            view0[k][m] = 'my_' + view0[k][m][:-1]
                        else:
                            view0[k][m] = 'other_' + view0[k][m][:-1]
                view1 = view0[::-1]
                view2 = [[view0[j][i] for j in range(len(view0))] for i in range(len(view0))]
                view3 = [row[::-1] for row in view2]
                # print(*view, sep='\n')
                for chip in self.snakes_chips[i]:
                    if self.is_match(view0, chip) or self.is_match(view0, chip.reversed()):
                        snake_move = (self.snakes[i][0][0] - 1, self.snakes[i][0][1])
                        # print('chip')
                        # print(*view0, sep='\n')
                    if self.is_match(view1, chip) or self.is_match(view1, chip.reversed()):
                        snake_move = (self.snakes[i][0][0] + 1, self.snakes[i][0][1])
                        # print('chip')
                        # print(*view1, sep='\n')
                    if self.is_match(view2, chip) or self.is_match(view2, chip.reversed()):
                        snake_move = (self.snakes[i][0][0], self.snakes[i][0][1] - 1)
                        # print('chip')
                        # print(*view2, sep='\n')
                    if self.is_match(view3, chip) or self.is_match(view3, chip.reversed()):
                        snake_move = (self.snakes[i][0][0], self.snakes[i][0][1] + 1)
                        # print('chip')
                        # print(*view3, sep='\n')
                    if snake_move not in snake_moves:
                        snake_move = None
                    else:
                        break
                if snake_move is None:
                    # print('not chip')
                    if len(snake_moves):
                        snake_move = choice(snake_moves)
                if snake_move is not None:
                    # print(self.board[snake_move[0]][snake_move[1]])
                    snakes_can_move += 1
                    if self.board[snake_move[0]][snake_move[1]] == 'empty4':
                        # print('empty')
                        self.board[self.snakes[i][-1][0]][self.snakes[i][-1][1]] = 'empty4'
                        self.snakes[i].pop()
                        self.board[self.snakes[i][-1][0]][self.snakes[i][-1][1]] = 'tail' + str(i)
                        self.board[self.snakes[i][0][0]][self.snakes[i][0][1]] = 'body' + str(i)
                        self.board[snake_move[0]][snake_move[1]] = 'head' + str(i)
                        self.snakes[i].insert(0, snake_move)
                    else:
                        self.board[self.snakes[i][0][0]][self.snakes[i][0][1]] = 'body' + str(i)
                        j = int(self.board[snake_move[0]][snake_move[1]][-1])
                        if len(self.snakes[j]):
                            self.snakes[j].pop()
                        if len(self.snakes[j]):
                            self.board[self.snakes[j][-1][0]][self.snakes[j][-1][1]] = 'tail' + str(j)
                        self.board[snake_move[0]][snake_move[1]] = 'head' + str(i)
                        self.snakes[i].insert(0, snake_move)
                # print(f'{i}: {snake_move}', self.snakes[i])
        return snakes_alive > 1 and snakes_can_move > 0

    def is_match(self, view, chip):
        if chip == chip.DEFAULT_BOARD:
            return False
        match_board = [[True] * len(view) for _ in range(len(view))]
        for i in range(len(view)):
            for j in range(len(view)):
                if chip.board[i][j] is not None:
                    match_board[i][j] = (view[i][j] == chip.board[i][j])
        for group in chip.groups_and.values():
            flag = True
            for i, j in group:
                flag = flag and match_board[i][j]
            if not flag:
                return False
        for group in chip.groups_or.values():
            flag = True
            for i, j in group:
                flag = flag or match_board[i][j]
            if not flag:
                return False
        for group in chip.groups_ex.values():
            for i, j in group:
                if match_board[i][j]:
                    return False
        return True

    def print(self):
        print('...' * self.width)
        for i in range(Board.K, self.width + Board.K):
            for j in range(Board.K, self.width + Board.K):
                print(Board.CELL_TYPES[self.board[i][j]], end=' ')
            print()
        # print('end')

    def get_score(self):
        return [len(self.snakes[i]) - Board.START_LEN_SNAKE for i in range(Board.N_SNAKES)]

    def set_view(self, new_left, new_top, new_cell_size):
        self.left = new_left
        self.top = new_top
        self.cell_size = new_cell_size

    def render(self):
        for i in range(Board.K, self.width + Board.K):
            for j in range(Board.K, self.width + Board.K):
                x, y = self.left + (j - Board.K) * self.cell_size, self.top + (i - Board.K) * self.cell_size
                pos = [x, y, self.cell_size, self.cell_size]
                if self.board[i][j] in ('wall4', 'empty4'):
                    pygame.draw.rect(self.screen, Board.CELL_COLORS[self.board[i][j]], pos)
                else:
                    pygame.draw.rect(self.screen, Board.CELL_COLORS['empty4'], pos)
                    pygame.draw.circle(self.screen, Board.CELL_COLORS[self.board[i][j]],
                                       [x + self.cell_size // 2, y + self.cell_size // 2],
                                       self.cell_size // 2 - 2)
                pygame.draw.rect(self.screen, Board.COLOR_BORDER, pos, 1)
