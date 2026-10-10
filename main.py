import pygame as pg
from dataclasses import dataclass
from pprint import pprint
from random import randint

pg.init()
screen = pg.display.set_mode((800, 800))  
events = pg.event.get()

HEAD = (255, 0, 0)
BODY = (0, 0, 255)
BOARD = (255, 255, 255)
FOOD = (0, 255, 0)

CELL_SIZE = 25
BOARD_SIZE = 25
CLOCK = pg.Clock()

@dataclass
class Cell():
    x :int
    y :int
    snake: str = None

    def draw(self,surface):
        if self.snake is not None:
            if self.snake == 'head':
                color = HEAD
            elif self.snake == 'body':
                color = BODY
            elif self.snake == 'food':
                color = FOOD
        else:
            color = BOARD

        rect = pg.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pg.draw.rect(surface, (color), rect)

state = [[Cell(x,y) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

def check_exit():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True

def draw_board():
    for row in state:
        for cell in row:
            cell.draw(screen)
    pg.display.flip()

def clear_board():
    for row in state:
        for cell in row:
            cell.snake = None
            full_snake.clear()

direction = 'right'
position_dict = {'right': [0, 1],
'left': [0, -1],
'up' : [-1, 0],
'down' : [1, 0] }
full_snake = []

def set_snake():
    x = BOARD_SIZE // 2
    y = BOARD_SIZE // 2
    y_d, x_d = position_dict[direction]
    state[y][x].snake = 'head'
    full_snake.append([state[y][x].y, state[y][x].x])
    if abs(x_d) > abs(y_d):
        for change in range (1,3):
            change *= -1 * x_d
            state[y][x + change].snake = 'body'
            full_snake.append([state[y][x + change].y, state[y][x + change].x])
    elif abs(x_d) < abs(y_d):
        for change in range (1,3):
            change *= -1 * y_d
            state[y + change][x].snake = 'body'
            full_snake.append([state[y + change][x].y ,state[y + change][x].x] )
            
def set_food():
    while True:
        x = randint(0, BOARD_SIZE - 1)
        y = randint(0, BOARD_SIZE - 1)
        if state[y][x].snake is None:
            state[y][x].snake = 'food'
            break

def check_collision(cell):
    if cell.snake is not None:
        if cell.snake == 'food':
            last = full_snake[len(full_snake) - 1]
            ex = full_snake[len(full_snake) - 2]
            full_snake.append([last[0] + (last[0]-ex[0]), last[1] + (last[1]-ex[1])])
            cell.snake = None
            set_food()
        if cell.snake == 'body':
            global direction
            running = True
            while running:
                for ev in pg.event.get():
                    if ev.type == pg.KEYDOWN:
                        if ev.key == pg.K_RIGHT:
                            direction = 'right' 
                            clear_board()
                            set_snake()
                            set_food()
                            running = False
                        elif ev.key == pg.K_LEFT: 
                            direction = 'left' 
                            clear_board()
                            set_snake()
                            set_food()
                            running = False
                        elif ev.key == pg.K_UP:
                            direction = 'up'
                            clear_board()
                            set_snake()
                            set_food()
                            running = False
                        elif ev.key == pg.K_DOWN:
                            direction = 'down'
                            clear_board()
                            set_snake()
                            set_food()
                            running = False
            return True
                            

def snake_move():
    for snake_piece in reversed(full_snake):
        y_d, x_d = position_dict[direction]
        y = snake_piece[0]
        x = snake_piece[1]
        cell = state[y][x]
        index = full_snake.index(snake_piece)
        if index != 0:
            last_cell = state[full_snake[index - 1][0]][full_snake[index - 1][1]]
            last_cell.snake = 'body'
            snake_piece[0] = last_cell.y
            snake_piece[1] = last_cell.x
            if index == len(full_snake) - 1:
                cell.snake = None
        if index == 0:
            new_y = y + y_d
            new_x = x + x_d
            if new_x < 0:
                new_x = BOARD_SIZE - 1
            if new_x >= BOARD_SIZE:
                new_x = 0 
            if new_y < 0:
                new_y = BOARD_SIZE - 1
            if new_y >= BOARD_SIZE:
                new_y = 0
            if not check_collision(state[new_y][new_x]):
                state[new_y][new_x].snake = 'head'
                snake_piece[0] = new_y
                snake_piece[1] = new_x


def move():
    global direction
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_RIGHT and direction != 'left':
                direction = 'right' 
                break
            elif ev.key == pg.K_LEFT and direction != 'right': 
                direction = 'left' 
                break
            elif ev.key == pg.K_UP and direction != 'down':
                direction = 'up'
                break
            elif ev.key == pg.K_DOWN  and direction != 'up':
                direction = 'down'
                break
        if ev.type == pg.QUIT:
            pg.quit()
    snake_move()
                  
running = True
while running:
    set_snake()
    set_food()
    while running:
        CLOCK.tick(3)
        move()
        draw_board()
        if check_exit():
            running = False