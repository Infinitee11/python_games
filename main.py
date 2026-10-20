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


state = [[[x, y] for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
full_snake = []
food = []

def check_exit():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True

def draw_board():
    for row in state:
        for cell in row:
            rect = pg.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen, BOARD, rect)
    

def draw_snake():
    for piece in full_snake:
        if full_snake.index(piece) == 0:
            color = HEAD
        else:
            color = BODY
        rect = pg.Rect(piece[0] * CELL_SIZE, piece[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pg.draw.rect(screen, color, rect)

def draw_food():
    for f in food:
        rect = pg.Rect(f[0] * CELL_SIZE, f[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pg.draw.rect(screen, FOOD, rect)

def draw():
    draw_board()
    draw_food()
    draw_snake()
    pg.display.flip()


def clear_board():
    for row in state:
        for cell in row:
            if cell[2] != 'food':
                cell[2] = None

direction = 'right'
position_dict = {'right': [0, 1],
'left': [0, -1],
'up' : [-1, 0],
'down' : [1, 0] }


def spawn_snake():
    full_snake.clear()
    x = BOARD_SIZE // 2
    y = BOARD_SIZE // 2
    y_d, x_d = position_dict[direction]
    full_snake.append([y, x, 'head'])
    if abs(x_d) > abs(y_d):
        for change in range (1,3):
            change *= -1 * x_d
            full_snake.append([x + change, y, 'body'])
    elif abs(x_d) < abs(y_d):
        for change in range (1,3):
            change *= -1 * y_d
            full_snake.append([x, y + change, 'body'])

            
def set_food():
    while True:
        set_food = True
        x = randint(0, BOARD_SIZE - 1)
        y = randint(0, BOARD_SIZE - 1)
        for piece in full_snake:
            if x == piece[0] and y == piece[1]:
                set_food = False
        if set_food:
            food.append([x, y])
            break

def move_snake():
    ex_head = full_snake[0]
    y_d, x_d = position_dict[direction]
    new_x = ex_head[0] + x_d
    new_y = ex_head[1] + y_d
    if check_collision() != 'food':
        full_snake.pop()
    else:
        food.pop()
        set_food()
    if new_x > BOARD_SIZE - 1:
        new_x = 0
    if new_y > BOARD_SIZE - 1:
        new_y = 0
    if new_x < 0:
        new_x = BOARD_SIZE - 1
    if new_y < 0:
        new_y = BOARD_SIZE - 1
    full_snake.insert(0, [new_x, new_y])

def check_collision():
    x = full_snake[0][0]
    y = full_snake[0][1]
    for f in food:
        if f[0] == x and f[1] == y:
            return 'food'
    
    for piece in full_snake[1:]:
        if x == piece[0] and y == piece[1]:
            food.clear()
            return "body"   
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
    move_snake()
                  
running = True
while running:
    running_snake = True
    spawn_snake()
    set_food()
    while running_snake:
        CLOCK.tick(3)
        move()
        draw()
        print(check_collision())
        if check_collision() == 'body':
            running_snake = False
        if check_exit():
            running = False