from random import choice, randint
import pygame
from os import path


def load_image(name, colorkey=None):
    fullname = path.join('data', name)
    img = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey)
    else:
        img = pygame.image.load(fullname).convert_alpha()
    return img


def load_snake_skin(names):
    skin = {'head': [load_image(names[0], -1)], 'body': [load_image(names[1], -1)],
            'turn': [load_image(names[2], -1)], 'tail': [load_image(names[3], -1)]}
    for k in skin.keys():
        skin[k].extend([pygame.transform.rotate(skin[k][0], 270),
                        pygame.transform.rotate(skin[k][0], 180),
                        pygame.transform.rotate(skin[k][0], 90)])
    x, y = False, True
    skin['turn'].extend([pygame.transform.flip(skin['turn'][i], x, y) for i in [2, 1, 0, 3]])
    return skin


class Board:
    N_SNAKES = 4
    START_LEN_SNAKE = 10
    K = 3
    CELL_TYPES = {'wall4': '##', 'empty4': '__',
                  'head0': 'O0', 'body0': '=0', 'tail0': '-0',
                  'head1': 'O1', 'body1': '=1', 'tail1': '-1',
                  'head2': 'O2', 'body2': '=2', 'tail2': '-2',
                  'head3': 'O3', 'body3': '=3', 'tail3': '-3'}

    CELL_COLORS = {'wall4': (0, 0, 0), 'empty4': (100, 100, 100),
                   'head0': (255, 0, 0), 'body0': (255, 0, 0), 'tail0': (255, 0, 0),
                   'head1': (102, 255, 0), 'body1': (102, 255, 0), 'tail1': (102, 255, 0),
                   'head2': (255, 204, 0), 'body2': (255, 204, 0), 'tail2': (255, 204, 0),
                   'head3': (0, 0, 179), 'body3': (0, 0, 179), 'tail3': (0, 0, 179)}
    COLOR_BORDER = (55, 55, 55)

    DIRECTIONS = {(1, 0): 'down', (0, -1): 'left', (-1, 0): 'up', (0, 1): 'right'}
    SKINS = {'head': 0, 'body': 1, 'turn': 2, 'tail': 3}

    def __init__(self, snakes_chips, skins, screen, n):
        self.width = self.height = n
        self.screen = screen
        self.left = 10
        self.top = 10
        self.cell_size = 25
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
        self.snakes_dir = [[['down'] for _ in range(len(self.snakes[0]))],
                           [['right'] for _ in range(len(self.snakes[1]))],
                           [['up'] for _ in range(len(self.snakes[2]))],
                           [['left'] for _ in range(len(self.snakes[3]))]]
        self.score = [1 * len(self.snakes[i]) for i in range(4)]
        for i in range(Board.N_SNAKES):
            if len(self.snakes[i]):
                self.board[self.snakes[i][0][0]][self.snakes[i][0][1]] = 'head' + str(i)
                self.board[self.snakes[i][-1][0]][self.snakes[i][-1][1]] = 'tail' + str(i)
                for x, y in self.snakes[i][1:-1]:
                    self.board[x][y] = 'body' + str(i)
        self.skins = skins
        self.snakes_skins = [load_snake_skin(skins[i]) for i in range(Board.N_SNAKES)]

    def step(self):
        snakes_alive = 0
        snakes_can_move = 0
        for i in range(Board.N_SNAKES):
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
                for chip in self.snakes_chips[i]:
                    if self.is_match(view0, chip) or self.is_match(view0, chip.reversed()):
                        snake_move = (self.snakes[i][0][0] - 1, self.snakes[i][0][1])
                    if self.is_match(view1, chip) or self.is_match(view1, chip.reversed()):
                        snake_move = (self.snakes[i][0][0] + 1, self.snakes[i][0][1])
                    if self.is_match(view2, chip) or self.is_match(view2, chip.reversed()):
                        snake_move = (self.snakes[i][0][0], self.snakes[i][0][1] - 1)
                    if self.is_match(view3, chip) or self.is_match(view3, chip.reversed()):
                        snake_move = (self.snakes[i][0][0], self.snakes[i][0][1] + 1)
                    if snake_move not in snake_moves:
                        snake_move = None
                    else:
                        break
                if snake_move is None:
                    if len(snake_moves):
                        snake_move = choice(snake_moves)
                if snake_move is not None:
                    snakes_can_move += 1
                    if self.board[snake_move[0]][snake_move[1]] == 'empty4':
                        self.board[self.snakes[i][-1][0]][self.snakes[i][-1][1]] = 'empty4'
                        self.snakes[i].pop()
                        next_dir = Board.DIRECTIONS[(snake_move[0] - self.snakes[i][0][0],
                                                     snake_move[1] - self.snakes[i][0][1])]
                        if next_dir not in self.snakes_dir[i][0]:
                            self.snakes_dir[i][0].append(next_dir)
                        self.snakes_dir[i].insert(0, [next_dir])
                        self.snakes_dir[i].pop()
                        self.snakes_dir[i][-1] = self.snakes_dir[i][-1][-1:]
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

                        next_dir = Board.DIRECTIONS[(snake_move[0] - self.snakes[i][0][0],
                                                     snake_move[1] - self.snakes[i][0][1])]
                        if next_dir not in self.snakes_dir[i][0]:
                            self.snakes_dir[i][0].append(next_dir)
                        self.snakes_dir[i].insert(0, [next_dir])
                        self.snakes_dir[j].pop()
                        self.board[snake_move[0]][snake_move[1]] = 'head' + str(i)
                        self.snakes[i].insert(0, snake_move)
        return snakes_alive >= 1 and snakes_can_move > 0

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

    def print(self, theme=0):
        print(' . ' * self.width)
        for i in range(Board.K, self.width + Board.K):
            for j in range(Board.K, self.width + Board.K):
                if theme == 0:
                    cell_str = Board.CELL_TYPES[self.board[i][j]]
                else:
                    k = int(self.board[i][j][-1])
                    if k == 4:
                        cell_str = Board.CELL_TYPES[self.board[i][j]]
                    else:
                        m = self.snakes[k].index((i, j))
                        if theme == 1:
                            cell_str = self.snakes_dir[k][m][0] + str(k + 1)
                        elif theme == 2:
                            if self.snakes_dir[k][m] in (['down'], ['up']):
                                cell_str = '|' + str(k + 1)
                            elif self.snakes_dir[k][m] in (['left'], ['right']):
                                cell_str = '-' + str(k + 1)
                            else:
                                cell_str = '.' + str(k + 1)
                        else:
                            if self.snakes_dir[k][m] in (['down'], ['up']):
                                cell_str = '|' + str(k + 1)
                            elif self.snakes_dir[k][m] in (['left'], ['right']):
                                cell_str = '-' + str(k + 1)
                            else:
                                if self.snakes_dir[k][m] in (['up', 'right'], ['right', 'up'],
                                                             ['down', 'left'], ['left', 'down']):
                                    cell_str = '/' + str(k + 1)
                                else:
                                    cell_str = '\\' + str(k + 1)

                print(cell_str, end=' ')
            print()

    def get_score(self):
        score = [None] * 4
        for i in range(4):
            if self.score[i]:
                score[i] = len(self.snakes[i]) - Board.START_LEN_SNAKE
        return score

    def set_view(self, new_left, new_top, new_cell_size):
        self.left = new_left
        self.top = new_top
        self.cell_size = new_cell_size

    def get_image_name(self, i, j, snake_ind):
        body_ind = self.snakes[snake_ind].index((i, j))
        if len(self.snakes_dir[snake_ind][body_ind]) == 2:
            return 'turn'
        return self.board[i][j][:-1]

    def get_image_rotate(self, snake_ind, body_ind):
        directions = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
        dirs = self.snakes_dir[snake_ind][body_ind]
        rotate = directions[dirs[0]]
        if len(self.snakes_dir[snake_ind][body_ind]) == 2:
            if directions[dirs[1]] - directions[dirs[0]] != 1 and directions[dirs[1]] - directions[dirs[0]] != -3:
                rotate += 4
        return rotate

    def render(self, theme=0):
        for i in range(Board.K, self.width + Board.K):
            for j in range(Board.K, self.width + Board.K):
                x, y = self.left + (j - Board.K) * self.cell_size, self.top + (i - Board.K) * self.cell_size
                pos = [x, y, self.cell_size, self.cell_size]
                if self.board[i][j] in ('wall4', 'empty4'):
                    pygame.draw.rect(self.screen, Board.CELL_COLORS[self.board[i][j]], pos)
                else:
                    pygame.draw.rect(self.screen, Board.CELL_COLORS['empty4'], pos)
                    if theme == 0:
                        pygame.draw.circle(self.screen, Board.CELL_COLORS[self.board[i][j]],
                                           [x + self.cell_size // 2, y + self.cell_size // 2],
                                           self.cell_size // 2 - 2)
                    else:
                        snake_ind = int(self.board[i][j][-1])
                        body_ind = self.snakes[snake_ind].index((i, j))
                        self.screen.blit(pygame.transform.scale(self.snakes_skins[snake_ind][
                                                                    self.get_image_name(i, j, snake_ind)
                                                                ][self.get_image_rotate(snake_ind, body_ind)],
                                                                (self.cell_size, self.cell_size)), pos)
                pygame.draw.rect(self.screen, Board.COLOR_BORDER, pos, 1)


class MiniBoard:
    CELL_COLORS = {'empty': (100, 100, 100), 'head': (255, 0, 0), 'body': (255, 0, 0), 'tail': (255, 0, 0)}
    COLOR_BORDER = (55, 55, 55)
    DIRECTIONS = {(1, 0): 'down', (0, -1): 'left', (-1, 0): 'up', (0, 1): 'right'}

    def __init__(self, skin, w, h, len_snake):
        self.width = w
        self.height = h
        self.len_snake = len_snake
        self.left = 10
        self.top = 10
        self.cell_size = 25
        self.board = [['empty'] * self.width for _ in range(self.height)]
        self.len_board = len(self.board)
        self.snake = [(0, i) for i in range(self.len_snake)]
        self.snake_dir = [['left'] for _ in range(len(self.snake))]
        self.board[self.snake[0][0]][self.snake[0][1]] = 'head'
        self.board[self.snake[-1][0]][self.snake[-1][1]] = 'tail'
        for x, y in self.snake[1:-1]:
            self.board[x][y] = 'body'
        self.skin = skin
        self.snake_skins = load_snake_skin(skin)

    def step(self):
        snake_move = (0, 0)  # доделать
        self.board[self.snake[-1][0]][self.snake[-1][1]] = 'empty'
        self.snake.pop()
        next_dir = MiniBoard.DIRECTIONS[(snake_move[0] - self.snake[0][0],
                                         snake_move[1] - self.snake[0][1])]
        if next_dir not in self.snake_dir[0]:
            self.snake_dir[0].append(next_dir)
        self.snake_dir.insert(0, [next_dir])
        self.snake_dir.pop()
        self.snake_dir[-1] = self.snake_dir[-1][-1:]
        self.board[self.snake[-1][0]][self.snake[-1][1]] = 'tail'
        self.board[self.snake[0][0]][self.snake[0][1]] = 'body'
        self.board[snake_move[0]][snake_move[1]] = 'head'
        self.snake.insert(0, snake_move)

    def set_view(self, new_left, new_top, new_cell_size):
        self.left = new_left
        self.top = new_top
        self.cell_size = new_cell_size

    def get_image_name(self, i, j):
        body_ind = self.snake.index((i, j))
        if len(self.snake_dir[body_ind]) == 2:
            return 'turn'
        return self.board[i][j]

    def get_image_rotate(self, body_ind):
        directions = {'up': 0, 'right': 1, 'down': 2, 'left': 3}
        dirs = self.snake_dir[body_ind]
        rotate = directions[dirs[0]]
        if len(self.snake_dir[body_ind]) == 2:
            if directions[dirs[1]] - directions[dirs[0]] != 1 and directions[dirs[1]] - directions[dirs[0]] != -3:
                rotate += 4
        return rotate

    def render(self, screen, theme=0):
        for i in range(self.height):
            for j in range(self.width):
                x, y = self.left + j * self.cell_size, self.top + i * self.cell_size
                pos = [x, y, self.cell_size, self.cell_size]
                pygame.draw.rect(screen, MiniBoard.CELL_COLORS[self.board[i][j]], pos)
                if self.board[i][j] != 'empty':
                    pygame.draw.rect(screen, MiniBoard.CELL_COLORS['empty'], pos)
                    if theme == 0:
                        pygame.draw.circle(screen, MiniBoard.CELL_COLORS[self.board[i][j]],
                                           [x + self.cell_size // 2, y + self.cell_size // 2],
                                           self.cell_size // 2 - 2)
                    else:
                        print(self.snake, (i, j))
                        body_ind = self.snake.index((i, j))
                        screen.blit(pygame.transform.scale(self.snake_skins[self.get_image_name(i, j)
                                                           ][self.get_image_rotate(body_ind)],
                                                           (self.cell_size, self.cell_size)), pos)
                pygame.draw.rect(screen, MiniBoard.COLOR_BORDER, pos, 1)
