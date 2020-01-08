import os
import random
import time


class Board:
    def __init__(self):
        self.board = self.create_board()
        self.board[12][12] = '*'
        self.x_pos0 = 12
        self.y_pos0 = 12
        
        self.body_pos_lst = []
        for i in range(1, 10):
            self.board[self.y_pos0 + i][self.x_pos0] = "#"
            self.body_pos_lst.append((self.x_pos0, self.y_pos0 + i))

    def create_board(self):
        board = [['.' for i in range(25)] for j in range(25)]
        return board
    
    def board_to_str(self):
        board_str = ''

        for string in self.board:
            for elem in string:
                board_str += elem + ' '
            board_str += "\n"
        
        return board_str

    def get_first_coord(self):
        return self.x_pos0, self.y_pos0
    
    def change_board(self, x_pos, y_pos, body_pos_lst):
        self.board = []
        self.board = self.create_board()
        self.board[y_pos][x_pos] = "*"
        self.body_pos_lst = body_pos_lst
        for coord in self.body_pos_lst:
            body_x, body_y = coord
            self.board[body_y][body_x] = '#'
    
    def get_body_position_lst(self):
        return self.body_pos_lst
 

class Snake:
    def __init__(self):
        self.board_obj = Board()
        self.x_pos, self.y_pos = self.board_obj.get_first_coord()
        self.body_pos_lst = self.board_obj.get_body_position_lst()
    
    def get_position(self):
        return self.x_pos, self.y_pos
    
    def set_new_position(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def change_pos_on_board(self):
        self.board_obj.change_board(self.x_pos, self.y_pos, self.body_pos_lst)

    def new_board_str(self):
        return self.board_obj.board_to_str()
    
    def get_body_pos_lst(self):
        return self.body_pos_lst

    def set_new_body_pos_lst(self, body_pos_lst):
        self.body_pos_lst = body_pos_lst


class Random_moving:
    def __init__(self):
        self.snake_obj = Snake()
        #флагами обозначено прошлое перемещение
        self.right = False
        self.left = False
        self.up = True #змейка не может идти вниз вначале
        self.down = False

        self.cant_move = False

        self.body_pos_lst = self.snake_obj.get_body_pos_lst()

        self.x, self.y = self.snake_obj.get_position()

    def get_new_coord(self):
        self.last_x, self.last_y = self.x, self.y
    
        choose_type_of_moving = random.choice(["by x", "by y"])

        self.step = False

        while self.step != True:
            if choose_type_of_moving == "by x":
                x_new = self.x_type_moving(self.x)
                y_new = self.y

                if self.cant_move:
                    self.cant_move = False
                    choose_type_of_moving = 'by y'

                if x_new > self.x:
                    self.right = True
                    self.left = False
                elif x_new < self.x:
                    self.left = True
                    self.right = False

                self.up = False
                self.down = False

            if choose_type_of_moving == 'by y':
                x_new = self.x
                y_new = self.y_type_moving(self.y)

                if self.cant_move:
                    self.cant_move = False
                    choose_type_of_moving = 'by x'
                
                if y_new > self.y:
                    self.down = True
                    self.up = False
                elif y_new < self.y:
                    self.up = True
                    self.down = False

                self.right = False
                self.left = False
            
            self.x, self.y = x_new, y_new

        return x_new, y_new
    
    #движение по оси x
    def x_type_moving(self, x):
        if self.right:
            if x == 24:
                possible_steps_x = [x]
                self.cant_move = True
            else:
                possible_steps_x = [x + 1]
        if self.left:
            if x == 0:
                self.cant_move = True
                possible_steps_x = [x]
            else:
                possible_steps_x = [x - 1]
        elif x == 24:
            possible_steps_x = [x - 1]
        elif x == 0:
            possible_steps_x = [x + 1]
        if not(self.right) and not(self.left) and x != 24 and x != 0:
            possible_steps_x = [x - 1, x + 1]
        
        if not(self.cant_move):
            possible_steps_x = self.check_lst_of_possibilities(x, self.y, possible_steps_x, "x")

            if possible_steps_x == False:
                exit(0)

            if possible_steps_x == [x]:
                self.cant_move = True

        if not(self.cant_move):
            self.step = True

        x = random.choice(possible_steps_x)

        return x
    
    #движение по оси y
    def y_type_moving(self, y):
        if self.up:
            if y == 0:
                self.cant_move = True
                possible_steps_y = [y]
            else:
                possible_steps_y = [y - 1]
        
        if self.down:
            if y == 24:
                self.cant_move = True
                possible_steps_y = [y]
            else:
                possible_steps_y = [y + 1]

        elif y == 24:
            possible_steps_y = [y - 1]
        elif y == 0:
            possible_steps_y = [y + 1]

        if not(self.up) and not(self.down) and y != 24 and y != 0:
            possible_steps_y = [y - 1, y + 1]

        if not(self.cant_move):
            possible_steps_y = self.check_lst_of_possibilities(self.x, y, possible_steps_y, 'y')
            if possible_steps_y == False:
                exit(0)

            if possible_steps_y == [y]:
                self.cant_move = True

        if not(self.cant_move):
            self.step = True

        y = random.choice(possible_steps_y)
        return y

    def check_lst_of_possibilities(self, x, y, lst_of_steps, check):
        local_lst = lst_of_steps.copy()

        if check == 'x':
            for i in range(len(lst_of_steps)):
                if (lst_of_steps[i], y) in self.body_pos_lst:
                    if len(local_lst) > 0:
                        if i >= len(local_lst):
                            return False
                        del local_lst[i]

            if len(local_lst) > 0:
                return local_lst
            else:
                return [x]
        else:
            for i in range(len(lst_of_steps)):
                if (x, lst_of_steps[i]) in self.body_pos_lst:
                    if len(local_lst) > 0:
                        if i >= len(local_lst):
                            return False
                        del local_lst[i]
            
            if len(local_lst) > 0:
                return local_lst
            else:
                return [y]

    def new_body_pos_lst(self):
        for i in range(len(self.body_pos_lst) - 1, 0, -1):
            self.body_pos_lst[i] = self.body_pos_lst[i - 1]
        
        self.body_pos_lst[0] = (self.last_x, self.last_y)

        return self.body_pos_lst

    def update_and_display(self):
        self.x, self.y = self.get_new_coord()
        self.snake_obj.set_new_position(self.x, self.y)
        self.body_pos_lst = self.new_body_pos_lst()
        self.snake_obj.set_new_body_pos_lst(self.body_pos_lst)
        self.snake_obj.change_pos_on_board()

        print(self.snake_obj.new_board_str())


obj1 = Random_moving()
obj_board = Board()
print(obj_board.board_to_str())

for i in range(500):
     obj1.update_and_display()
     time.sleep(0.1)