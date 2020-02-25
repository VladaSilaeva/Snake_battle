from chips import Chip
from board import Board, MiniBoard
from snake_menu import Snake
import pygame, sys


left = top = 0
cell_size = 25
n_cell = 25
size = W, H = n_cell * cell_size , n_cell * cell_size
pygame.init()
screen = pygame.display.set_mode(size)
main_color = pygame.Color('lightskyblue3')
FONT = pygame.font.Font(None, 50)
FONT_2 = pygame.font.Font(None, 30)
snakes = [Snake()]


class Button:
    def __init__(self, x, y, w, h, text='', font=FONT):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = main_color
        self.text = text
        self.font = font
        self.txt_surface = FONT.render(text, True, self.color)
        self.func = None

    def draw(self, screen):
        self.txt_surface = self.font.render(self.text, True, self.color)
        if self.font == FONT:
            screen.blit(self.txt_surface, (self.rect.x + self.rect.width // 2 - len(self.text) * (self.rect.width // 20), self.rect.y + self.rect.height // 4))
        else:
            screen.blit(self.txt_surface, (self.rect.x + self.rect.width // 2 - len(self.text) * (self.rect.width // 15), self.rect.y + self.rect.height // 4))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*event.pos):
                if self.func is not None:
                    self.func()


class SnakeInfo:
    def __init__(self, x, y, w, h, snake_ind=None):
        self.rect = pygame.Rect(x, y, w, h)
        d = 10
        w_btn, h_btn = w // 2 - d, 50
        self.btn_change = Button(x, y + h - h_btn, w_btn, h_btn, 'change', FONT_2)
        self.btn_change.func = lambda: change_snake(self)
        self.btn_edit = Button(x + w - w_btn, y + h - h_btn , w_btn, h_btn, 'create', FONT_2)
        self.btn_edit.func = lambda: create_snake(self)
        self.snake_ind = snake_ind
        self.color = main_color
        self.text = ['', '']
        self.active = False
        self.mini_board = None
        if snake_ind is not None:
            self.text = ['Name: ' + snakes[snake_ind].name, 'Score: ' + str(snakes[snake_ind].rang)]
            self.mini_board = MiniBoard(snakes[snake_ind].skin, 5, 2, 4)
            self.btn_edit.text = 'edit'
            self.btn_edit.func = lambda: edit_snake(snake_ind)
        self.txt_surface = [FONT.render(text, True, self.color) for text in self.text]

    def draw(self, screen):
        self.txt_surface = [FONT_2.render(text, True, self.color) for text in self.text]
        screen.blit(self.txt_surface[0], (self.rect.x + self.rect.width // 2 - len(self.text) * (self.rect.width // 20), self.rect.y + self.rect.height // 4))
        pygame.draw.rect(screen, self.color, self.rect, 4)
        self.btn_edit.draw(screen)
        self.btn_change.draw(screen)
        if self.snake_ind is not None:
            self.mini_board.render(screen, theme=1)

    def update(self):
        if self.active:
            self.mini_board.step()

    def handle_event(self, event):
        self.btn_edit.handle_event(event)
        self.btn_change.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*event.pos):
                self.active = False if self.active else True


def terminate():
    pygame.quit()
    sys.exit()


def change_snake(snake_info):
    print('change')


def create_snake(snake_info):
    print('create')


def edit_snake(i):
    print('edit')


def start_screen():
    clock = pygame.time.Clock()
    buttons = []
    n = 2
    width = 200
    height = 50
    top = (size[0] - n * height) // 2
    for i in range(n):
        buttons.append(Button((size[1] - width) // 2, top + i * height * 2, width, height))
    buttons[0].text = 'Start'
    buttons[0].func = start
    buttons[-1].text = 'Exit'
    buttons[-1].func = terminate
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            for box in buttons:
                box.handle_event(event)

        screen.fill((30, 30, 30))
        for box in buttons:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def start():
    ch = []
    ch.append(Chip([[None, None, None, 'other_tail', 'other_tail', 'other_tail', 'other_tail'],
                    [None, None, None, 'other_tail', 'other_tail', 'other_tail', None],
                    [None, None, None, 'other_tail', 'other_tail', None, None],
                    [None, None, None, 'my_head', None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None]],
                   groups_or={'or0': [(0, 3), (0, 4), (0, 5), (0, 6), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4)]}))
    ch.append(Chip([[None, None, None, None, None, None, None],
                    [None, None, None, 'empty', None, None, None],
                    [None, None, None, 'empty', None, None, None],
                    [None, None, None, 'my_head', None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None]], ))
    ch.append(Chip([[None, None, None, 'empty', None, None, None],
                    [None, None, None, 'empty', None, None, None],
                    [None, None, None, 'empty', None, None, None],
                    [None, None, None, 'my_head', None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None]], ))
    ch.append(Chip([[None, None, 'empty', 'empty', 'empty', None, None],
                    [None, None, 'empty', 'empty', 'empty', None, None],
                    [None, None, None, 'empty', None, None, None],
                    [None, None, None, 'my_head', None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None]], ))
    ch.append(Chip([[None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, 'other_tail', None, None, None],
                    [None, None, None, 'my_head', None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None],
                    [None, None, None, None, None, None, None]], ))
    snakes.append(Snake('snake1(4 chips)', [ch[3], ch[2], ch[1], ch[4]]))
    snakes.append(Snake('snake2(rand)', [Chip()]))
    snakes.append(Snake('snake3(1 chip)', [ch[4]]))

    snakes_cur = [0 for i in range(4)]
    snakes_cur[0] = 1
    snakes_cur[1] = 2
    snakes_cur[2] = 3
    snakes[1].skin = ['head_1.png', 'body_1.png', 'turn_1.png','tail_1.png']
    snakes[2].skin = ['head_2.png', 'body_2.png', 'turn_2.png','tail_2.png']


    text = '''ЗМЕЙКИ'''
    print(text)
    # start_game(snakes_cur)

    clock = pygame.time.Clock()
    buttons = []
    n = 3
    width = 200
    height = 50
    #top = (size[0] - n * height) // 2
    top = 15
    for i in range(n):
        buttons.append(Button((400 + size[1] - width) // 2, top + i * height * 2, width, height))
    buttons[0].text = 'Start Game'
    buttons[0].func = lambda: start_game(snakes_cur)
    buttons[1].text = 'Main Menu'
    buttons[1].func = start_screen
    buttons[-1].text = 'Exit'
    buttons[-1].func = terminate
    snakes_info = [SnakeInfo(0, top, width, width, 1),
                   SnakeInfo(width + 10, top, width, width, 2),
                   SnakeInfo(0, top + width + 10, width, width, 3),
                   SnakeInfo(width + 10, top + width + 10, width, width)]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            for box in buttons:
                box.handle_event(event)
            for info in snakes_info:
                info.handle_event(event)

        screen.fill((30, 30, 30))
        for box in buttons:
            box.draw(screen)
        for info in snakes_info:
            info.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def start_game(snakes_ind):
    snakes_chips = [snakes[i].chips for i in snakes_ind]
    skins = [snakes[i].skin for i in snakes_ind]
    board = Board(snakes_chips, skins, screen, 25)
    board.set_view(left, top, cell_size)
    color_background = (0, 0, 0)
    v = 20
    clock = pygame.time.Clock()
    running = True
    do_move = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    v += 2
                elif event.button == 5:
                    if v > 2:
                        v -= 2
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if do_move:
                        do_move = False
                    else:
                        do_move = True
                if event.key == pygame.K_ESCAPE:
                    running = False
        if do_move:
            running = board.step() and running
        screen.fill(color_background)
        board.render(theme=1)
        for i in range(4):
            print(board.snakes_dir[i])
        print()
        pygame.display.flip()
        clock.tick(v)

    score = board.get_score()
    print(score)
    score_text = ["", "Score", "", "", ""]
    for i in range(4):
        if score[i] is None:
            score_text.append('')
        else:
            score_text.append(str(snakes[snakes_ind[i]]) + ' + ' * (score[i] >= 0) + ' - ' * (score[i] < 0) + str(abs(score[i])))
            snakes[snakes_ind[i]].rang += score[i]

    screen.fill(color_background)
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in score_text:
        string_rendered = font.render(line, 2, main_color)
        score_rect = string_rendered.get_rect()
        text_coord += 10
        score_rect.top = text_coord
        score_rect.x = (W - score_rect.width) // 2
        text_coord += score_rect.height
        screen.blit(string_rendered, score_rect)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                running = False
                if event.key == pygame.K_r:
                    return start_game(snakes_ind)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        pygame.display.flip()
        clock.tick(v)


def main():
    start_screen()


if __name__ == '__main__':
    main()
    pygame.quit()
