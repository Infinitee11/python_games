import pygame as pg
from dataclasses import dataclass
from pprint import pprint

pg.init()
screen = pg.display.set_mode((800, 800))  

HEAD = (255, 0, 0)
BODY = (0, 0, 255)
BOARD = (255, 255, 255)

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
        else:
            color = BOARD

        rect = pg.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pg.draw.rect(surface, (color), rect)
        pg.display.flip()

state = [[Cell(x,y) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

def draw_board():
    for row in state:
        for cell in row:
            cell.draw(screen)

direction = 'right'
position_dict = {'right': [0, 1],
'left': [0, -1],
'up' : [1, 0],
'down' : [-1, 0] }
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
            
def snake_move():
    print(full_snake)
    for snake_piece in reversed(full_snake):
        y_d, x_d = position_dict[direction]
        y = snake_piece[0]
        x = snake_piece[1]
        cell = state[y][x]
        index = full_snake.index(snake_piece)
        if index != 0:
            last_cell = state[full_snake[index - 1][0]][full_snake[index - 1][1]]
            # last_snake_piece = full_snake[index - 1]
            last_cell.snake = 'body'
            snake_piece[0] = last_cell.y
            snake_piece[1] = last_cell.x
            if index == len(full_snake) - 1:
                cell.snake = None
        if index == 0:
            state[y + y_d][x + x_d].snake = 'head'
            snake_piece[0] += y_d
            snake_piece[1] += x_d
        # print(full_snake)

                  
    # def set_position(self, position):
    #     x, y = position

    #     if x < 0:
    #         x = BOARD_SIZE - 1
    #     if x >= BOARD_SIZE:
    #         x = 0 
    #     if y < 0:
    #         y = BOARD_SIZE - 1
    #     if y >= BOARD_SIZE:
    #         y = 0

    #     self.position = [x, y]

        # move = self.state.direction
        # for ev in pg.event.get():
        #     if ev.type == pg.KEYDOWN:
        #         if ev.key == pg.K_RIGHT:
        #             move = 'right'
        #         elif ev.key == pg.K_LEFT:
        #             move = 'left'
        #         elif ev.key == pg.K_UP:
        #             move = 'up'
        #         elif ev.key == pg.K_DOWN:
        #             move = 'down'

        #     elif ev.type == pg.QUIT:
        #         pg.quit()

        # self.state.direction = move
        # self.state.move()




running = True
while running:
    set_snake()
    while running:
        CLOCK.tick(3)
        draw_board()
        snake_move()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False